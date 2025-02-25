SELECT * 
FROM layoffs;

-- Creating a backup table
CREATE TABLE layoffs_staging
LIKE layoffs; 

-- Coping insides of original table into a new one
INSERT layoffs_staging
SELECT *
FROM layoffs;

-- Checking if any duplicates are present
SELECT * ,
ROW_NUMBER() OVER ( 
PARTITION BY company, industry, total_laid_off, percentage_laid_off, `date`) AS row_num
FROM layoffs_staging;

-- Finding all duplicates
WITH duplicate_cte AS
(
SELECT * ,
ROW_NUMBER() OVER ( 
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
SELECT * 
FROM duplicate_cte
WHERE row_num > 1;

-- Checking if for sure for Casper company there is a duplicate
SELECT * 
FROM layoffs_staging
WHERE company = 'Casper';

-- Trying to delete duplicates using CTE, but it doesn't work in MySQL
WITH duplicate_cte AS
(
SELECT * ,
ROW_NUMBER() OVER ( 
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging
)
DELETE
FROM duplicate_cte
WHERE row_num > 1;

-- Creating new table with row number being present
CREATE TABLE `layoffs_staging_2` (
  `company` text,
  `location` text,
  `industry` text,
  `total_laid_off` int DEFAULT NULL,
  `percentage_laid_off` text,
  `date` text,
  `stage` text,
  `country` text,
  `funds_raised_millions` int DEFAULT NULL,
  `row_number` int
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Inserting the data from previous table
INSERT INTO layoffs_staging_2
SELECT * ,
ROW_NUMBER() OVER ( 
PARTITION BY company, location, industry, total_laid_off, percentage_laid_off, `date`, stage, country, funds_raised_millions) AS row_num
FROM layoffs_staging;

-- Double checking rows to delete
SELECT * 
FROM layoffs_staging_2
WHERE `row_number` > 1;

-- Enabling deleting full row numbers and similar actions
SET SQL_SAFE_UPDATES = 0;

-- Deleting all duplicates
DELETE
FROM layoffs_staging_2
WHERE `row_number` > 1;

-- Testing trimming to eliminate not needed spaces in upcoming step as this problem was spotted
SELECT DISTINCT company, TRIM(company)
FROM layoffs_staging_2;

-- Performing trimming of company column
UPDATE layoffs_staging_2
SET company = TRIM(company);

-- Checking if the issue with not needed spaces is the same for industry
SELECT DISTINCT industry
FROM layoffs_staging_2
ORDER BY 1;

-- There is different issue with Crypto and Crypto&, investigating to make sure how to react
SELECT *
FROM layoffs_staging_2
WHERE Industry LIKE 'Crypto%';

-- Unification of Crypto% to just Crypto
UPDATE layoffs_staging_2
SET industry = 'Crypto'
WHERE Industry LIKE 'Crypto%';

-- Checking for any similar issues with country column
SELECT DISTINCT country
FROM layoffs_staging_2
ORDER BY 1;

-- Unification of United States% into United States
UPDATE layoffs_staging_2
SET country = 'United States'
WHERE country LIKE 'United States%';

-- Eliminating not needed '.' on the end of 'United States.' variation
UPDATE layoffs_staging_2
SET country = TRIM(TRAILING '.' FROM country)
WHERE country LIKE 'United States.';

-- Validating proper way to transoform dete column into date format
SELECT `date`,
STR_TO_DATE (`date`, '%m/%d/%Y')
FROM layoffs_staging_2;

-- Transforming values in date column into date format
UPDATE layoffs_staging_2
SET `date` = STR_TO_DATE (`date`, '%m/%d/%Y');

-- Transforming type of values into date type
ALTER TABLE layoffs_staging_2
MODIFY COLUMN `date` DATE;

-- Investigating Null values for laid_off data columns
SELECT * 
FROM layoffs_staging_2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

-- Investigating NULL or empty industry values
SELECT *
FROM layoffs_staging_2
WHERE industry is NULL
OR industry ='';

-- Double checking on example if we can copy industry from another row
SELECT *
FROM layoffs_staging_2
WHERE company = 'AirBnb';

-- Trying join for fulfilling empty industry fields from the rows which have same companies/locations
SELECT *
FROM  layoffs_staging_2 st1
JOIN layoffs_staging_2 st2
	ON st1.company = st2.company
    AND st1.location = st2.location
WHERE (st1.industry IS NULL OR st1.industry = '')
AND st2.industry IS NOT NULL;

-- As upper join was not working trying to replace '' industry field with NULL to simplify further operation 
UPDATE layoffs_staging_2
SET industry = NULL
WHERE industry = '';

-- Updating with join those rows which have null values and can 'borrow' industry from different row with same company
UPDATE layoffs_staging_2 st1
JOIN layoffs_staging_2 st2
	ON st1.company = st2.company
SET st1.industry = st2.industry
WHERE (st1.industry IS NULL)
AND st2.industry IS NOT NULL;

-- Investigating null values for laid_off columns
SELECT * 
FROM layoffs_staging_2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

-- Deleting rows where for both of the mentioned columns data is null as those will be useless for us
DELETE
FROM layoffs_staging_2
WHERE total_laid_off IS NULL
AND percentage_laid_off IS NULL;

-- Checking final results
SELECT * FROM layoffs_staging_2;

-- Droping row_number column
ALTER TABLE layoffs_staging_2
DROP COLUMN `row_number` ;

