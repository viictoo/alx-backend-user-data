## 0x00-personal_data

### Personally identifiable information (PII) :
Any data that can be used to identify someone

Examples:
1. Full name
2. Social Security number (SSN)
3. Date of birth
4. Address (including street address, city, state, and ZIP code)
5. Phone number
6. Email address
7. Driver's license number
8. Passport number
9. Financial information (bank account number, credit card number)
10. Biometric data (fingerprint, iris scan)

Implementing a log filter to obfuscate PII fields:
To obfuscate PII fields in log files, you can use techniques like data masking or redaction.
Here's a high-level approach:

1. Identify the PII fields in your log data. This could include fields like names, email addresses, or phone numbers.
2. Determine the level of obfuscation required. You might choose to completely mask certain PII fields
 (e.g., replacing the entire value with asterisks), while for others, you might only partially obfuscate them (e.g., replacing all but the last few digits of a credit card number).
3. Implement a log filter or parsing mechanism that intercepts log messages before they are written to
 disk or sent to a logging service.
4. Apply the obfuscation logic to the identified PII fields in each log message.
5. Replace the original PII values with the obfuscated versions.
6. Proceed with the regular logging process, storing the obfuscated log messages.

It's important to consider security and compliance requirements when implementing PII obfuscation.using applicable regulations and best practices for handling PII, eg
- General Data Protection Regulation (GDPR)  EU privacy law and human rights law that aims to protect the personal data of individuals and enhance their control over it.
- Health Insurance Portability and Accountability Act (HIPAA). governing patient privacy
- Children’s Online Privacy Protection Act (COPPA), designed to protect the personal information of children under the age of 13

Encrypting a password and checking its validity:
To encrypt a password, use a strong, industry-standard cryptographic algorithm like
bcrypt or Argon2.
Here's a general outline of the process:

1. Generate a random salt value. A salt is a random data added to the password before hashing
    to prevent precomputed lookup tables (rainbow tables) from being used to crack the password.
2. Combine the salt value with the password.
3. Hash the combined salt and password using a secure hashing algorithm.
4. Store the resulting hash and the salt value in a secure manner (e.g., in a database).
   Note: It's important not to store the plain-text password.

To check the validity of an input password:

1. Retrieve the stored salt and hash associated with the user's password.
2. Combine the salt with the input password.
3. Hash the combined salt and input password using the same secure hashing algorithm.
4. Compare the resulting hash with the stored hash.
5. If the hashes match, the input password is valid.

By comparing the hashes instead of the plain-text passwords,
you can verify the correctness of the input password without
exposing the actual password value.

Authenticating to a database using environment variables:

1. Determine the required credentials for database authentication.
    This typically includes a username and password.
2. Set the necessary environment variables in your deployment environment or
  configuration file. For example, DB_USERNAME` and `DB_PASSWORD
3. In your application code, access the environment variables and retrieve the database credentials.
4. Use the retrieved credentials to establish a connection to the database using the appropriate
    database driver or client library.
5. Perform the necessary authentication steps provided by the database driver or library,
    passing in the retrieved credentials.
6. If the authentication is successful, you can proceed with interacting with the database.

By using environment variables, you can separate sensitive information like database credentials
from your codebase and configuration files, reducing the risk of accidental exposure or version
control mishaps.
