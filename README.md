# Telegram Account Manager

A tool for managing Telegram accounts, including spam removal and account validation.

## Features
- **Account Validation**: Validates Telegram accounts using provided credentials.
- **Spam Removal**: Automates the process of removing spam blocks from accounts.
- **Privacy Settings**: Updates privacy settings for Telegram accounts.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/telegram-account-manager.git
   cd telegram-account-manager
   
# Files description 

**accounts**:
This folder contains subdirectories for various Telegram accounts that are being managed by the tool. Each subdirectory is named after the phone number associated with the account or a unique identifier. Inside these subdirectories, you will find the tdata folder, which contains Telegram session data files.

**accounts2**:
This folder is used for storing Telegram accounts that have been successfully processed or transferred. The folder structure is similar to the accounts folder, with each subdirectory containing a tdata folder for the session data.

**spam**:
This folder contains Telegram accounts that have been identified as having spam issues. These accounts require further attention, such as attempting to remove spam blocks.

**снятие спама**:
This folder stores accounts that have had spam blocks successfully removed. It serves as an archive of accounts that have been processed for spam removal.

**не удалось**:
This folder contains accounts that could not be processed successfully. These accounts might have encountered errors during validation or spam removal and need to be reviewed manually.

**невалидные_аккаунты**:
This folder stores accounts that have been determined to be invalid or unusable. These accounts failed the validation checks and are archived here for record-keeping.

**не проверен**:
This folder is a temporary storage area for accounts that have not yet been processed or validated. Accounts placed here are awaiting further action.
