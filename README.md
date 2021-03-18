# Google_Doc_AI_Lambda_Snowflake
Code Snippet to integrate Google Document AI with Snowflake from a Lambda function

### Requirements:
##### 1. Google Cloud account 
A Google Cloud account with Document AI APIs Enabled
##### 2. Snowflake Account 
A Snowflake account, ideally running in GCP
##### 3. Lambda
You will need a Lambda in AWS with external access.  This is by default if you do not assign the Lambda to a VPC.
##### 4. Documents
I used IRS 1040 Sample documents, all containing the same information, but of different qualities, skewness, and rotations.  Please contanct me for help getting some documents if needed.

### Setup:
To run this system:
1. Create your table in Snowflake to land the structured data extracted from the documents
2. Verify your Snowflake credentials
3. Verify your Document AI REST API call
4. Verify your Python locally
5. Deploy your Python from Lambda
