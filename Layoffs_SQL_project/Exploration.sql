-- Maximums on laid_off values
SELECT MAX(total_laid_off), MAX(percentage_laid_off)
 FROM  layoffs_staging_2;
 
 -- Companies which laid_off all employees, ordered by funds raised
 SELECT *
 FROM layoffs_staging_2
 WHERE percentage_laid_off = 1
 ORDER BY funds_raised_millions DESC;
 
 -- Layoffs total grouped by companies 
SELECT company, SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY company
 ORDER BY 2 DESC;
 
 -- Date range of layoffs in the file
 SELECT MIN(`date`), MAX(`date`)
 FROM layoffs_staging_2;
 
 -- Total layoffs based on industry, ordered to focus on the biggest ones
 SELECT industry, SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY industry
 ORDER BY 2 DESC;
 
 -- Just investigating
 SELECT * 
 FROM layoffs_staging_2;
 
 -- Total layoffs per country
SELECT country, SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY country
 ORDER BY 2 DESC;
 
 -- Total layoffs per year
SELECT YEAR(`date`), SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY YEAR(`date`)
 ORDER BY 2 DESC;
 
 -- Total layoffs per stage of the companies
 SELECT stage, SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY stage
 ORDER BY 2 DESC;

 
 -- Total layoffs per month
 SELECT substring(`date`,1,7) AS month, SUM(total_laid_off)
 FROM layoffs_staging_2
 WHERE substring(`date`,1,7) IS NOT NULL
 GROUP BY substring(`date`,1,7)
 ORDER BY substring(`date`,1,7);

 -- All layoffs per each month (taking into consideration different months for different years)
 WITH rolling_total AS
 (
  SELECT substring(`date`,1,7) as `MONTH`, SUM(total_laid_off) AS total_off
 FROM layoffs_staging_2
 WHERE substring(`date`,1,7) IS NOT NULL
 GROUP BY substring(`date`,1,7)
 ORDER BY substring(`date`,1,7)
 )
 SELECT `MONTH`, SUM(total_off) OVER(ORDER BY `MONTH`) AS rolling_total, total_off
 FROM rolling_total;
 
 -- Total layoffs by companies (from biggest)
 SELECT company, SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY company
 ORDER BY 2 DESC;
 
 -- Total layoffs by company an year
 SELECT company, YEAR(`date`), SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY company, YEAR(`date`)
 ORDER BY company ASC;
 
 -- Biggest layoffs for particular companies and years
  SELECT company, YEAR(`date`), SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY company, YEAR(`date`)
 ORDER BY 3 DESC;
 
 -- Top 5 biggest layoffs by companies each year
 WITH company_year(company, years, total_laid_off) AS
 (
  SELECT company, YEAR(`date`), SUM(total_laid_off)
 FROM layoffs_staging_2
 GROUP BY company, YEAR(`date`)
 ORDER BY company ASC
 ), company_year_rank AS
 (
 SELECT *, DENSE_RANK() OVER (PARTITION BY years ORDER BY total_laid_off DESC) AS ranking
 FROM company_year
 WHERE years IS NOT NULL
 )
 SELECT * 
 FROM company_year_rank
 WHERE ranking <= 5
 ORDER BY ranking ASC;
 
 SELECT * 
  FROM layoffs_staging_2;
  
  
-- Cumulative laid offs shown with all of layoff events numbering present
SELECT 
    company,
    location,
    date,
    total_laid_off,
    SUM(total_laid_off) OVER (PARTITION BY company ORDER BY date) AS cumulative_laid_off,
    ROW_NUMBER() OVER (PARTITION BY company ORDER BY date) AS event_number
FROM layoffs_staging_2
ORDER BY company, date;

-- Comparison between total company layoffs and average for similar sums in desired country
WITH company_summaries AS (
    SELECT 
        company,
        country,
        SUM(total_laid_off) AS total_by_company
    FROM layoffs_staging_2
    GROUP BY company, country
)
SELECT 
    company,
    total_by_company,
    AVG(total_by_company) OVER (PARTITION BY country) AS average_laid_off_in_country
FROM company_summaries
ORDER BY company;
