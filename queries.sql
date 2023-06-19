CREATE TABLE IF NOT EXISTS employers(
                        company_id int PRIMARY KEY,
                        company_name varchar
                    );

CREATE TABLE IF NOT EXISTS vacancies(
                        vacancy_id int PRIMARY KEY,
                        vacancy_name varchar,
                        url varchar,
                        salary_from int,
                        salary_to int,
                        company int REFERENCES employers(company_id)
                    );

INSERT INTO employers (company_id, company_name) VALUES ('{employers_id}', '{company_name}')
ON CONFLICT (company_id) DO NOTHING

INSERT INTO vacancies (vacancy_id, vacancy_name, url, salary_from, salary_to, company)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (vacancy_id) DO NOTHING

SELECT company_name, COUNT(vacancy_name) as vacancies
FROM vacancies
INNER JOIN employers ON vacancies.company = employers.company_id
GROUP BY company_name

SELECT company_name, vacancy_name, salary_from, salary_to, url FROM vacancies
INNER JOIN employers ON vacancies.company = employers.company_id

SELECT company_name, AVG(salary_from) as avg_salary
FROM vacancies
INNER JOIN employers ON vacancies.company = employers.company_id
GROUP BY company_name

ELECT vacancy_name, MAX(salary_from) as max_salary
FROM vacancies
GROUP BY vacancy_name

SELECT vacancy_name FROM vacancies
WHERE vacancy_name LIKE '%{keyword}
