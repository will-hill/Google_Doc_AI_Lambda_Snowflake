USE DEMO_DB;
USE ROLE accountadmin;

--------------------------------------------------------------------------------------------------------

-- TRUNCATE TABLE form_1040;
SELECT * FROM form_1040;

--------------------------------------------------------------------------------------------------------
-- DDL -- CREATE TABLE TO STORE Document AI Data

CREATE OR REPLACE TABLE form_1040 (
  Year  STRING,
  FilingStatusCheckbox STRING,
  FirstName STRING,
  LastName STRING,
  AddressStreet STRING,
  AddressApt STRING,
  AddressCityStateZip STRING,
  SSN STRING,
  WagesSalariesTips DOUBLE,
  SocialSecurityBenefits DOUBLE,
  TotalIncome	DOUBLE
);

--------------------------------------------------------------------------------------------------------
-- DDL:JSON -- CREATE TABLE TO STORE Document AI Data JSON

-- CREATE OR REPLACE TABLE  form_1004_json (form_raw_json_data variant);
-- TRUNCATE TABLE form_1004_json;
-- SELECT * FROM form_1004_json;

SELECT 
    form_raw_json_data:"Property Address",
    form_raw_json_data:"City",
    form_raw_json_data:"State",
    form_raw_json_data:"Zip Code"
FROM form_1004_json;
  
SELECT form_raw_json_data:Borrower   FROM form_1004_json;
SELECT form_raw_json_data:City       FROM form_1004_json;
SELECT form_raw_json_data:"Zip Code" FROM form_1004_json;
