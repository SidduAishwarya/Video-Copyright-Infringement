# Video Copyright Infringement Detection and Protection

## Overview
This project aims to detect and protect against copyright infringement of videos by using perceptual hashing on the Ethereum blockchain. It allows users to register their videos, generate a unique hash, and verify the integrity of their content when re-uploaded.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Features
- **Perceptual Hashing**: Generate unique hashes for videos to compare content integrity.
- **Blockchain Integration**: Store video hashes on the Ethereum blockchain for secure and tamper-proof storage.
- **Hash Comparison**: Automatically compare newly uploaded videos with registered hashes to determine if the content has been edited or is the same as the original.
- **User Interface**: A simple and intuitive frontend for users to upload videos and view results.

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Node.js, Express.js
- **Blockchain**: Ethereum, Solidity
- **Development Tools**: Remix IDE, VS Code

## Installation

### Prerequisites
- Node.js (v14 or later)
- npm (Node Package Manager)
- Ganache (for local Ethereum blockchain testing)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/video-copyright-infringement.git
   cd video-copyright-infringement
2. Install Backend Dependencies
Navigate to the backend directory and install the necessary Python dependencies using the requirements.txt file:

   ```bash
   cd backend
   pip install -r requirements.txt

3. Install Frontend Dependencies
Navigate to the frontend directory and install the necessary Node.js dependencies:

   ```bash
   cd ../frontend
   npm install

4. Set Up Ganache
Set up Ganache and deploy the Solidity contracts using Remix IDE.
5. Start the Backend Server
Start the backend server using the following command:

   ```bash
   python app.py

6. Open the Frontend
Open the frontend in your browser by navigating to http://localhost:3000.
Usage
Upload a video file through the frontend.
The application generates a perceptual hash for the video and registers it on the Ethereum blockchain.
If the same video or a modified version is uploaded later, the application
compares its hash with the registered hash and notifies the user if it 
has been altered or is identical.


## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
