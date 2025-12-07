# 🔐 Image Encryption & Decryption Web Application

This project is a secure web-based tool that allows users to encrypt and decrypt images using strong AES-256 encryption. Designed with a focus on privacy and modern cybersecurity practices, the application ensures that sensitive images remain protected during storage or transfer. The interface is simple, clean, and responsive, allowing users to handle encryption tasks effortlessly.

---

## 📌 Key Features

* **AES-256 Encryption:** Converts images into unreadable encrypted data.
* **Password-Protected Decryption:** Images can only be restored with the correct password.
* **Automatic File Handling:** Encrypted and decrypted files download instantly.
* **Live Preview:** Users can preview uploaded and decrypted images safely.
* **Secure Cryptographic Workflow:** Includes salt, IV generation, and PBKDF2-based key derivation.
* **Modern UI:** Smooth animations, clean layout, and intuitive user experience.

---

## 🧠 How the System Works

### 🔒 Encryption

1. User selects an image.
2. The system validates the file type.
3. The image preview appears.
4. User enters a password.
5. AES-256 is applied to encrypt the image.
6. The encrypted file downloads automatically.

### 🔓 Decryption

1. User uploads the encrypted file.
2. Password is verified and the key is rebuilt.
3. AES decrypts the content.
4. The original image is restored and displayed.
5. The decrypted file is automatically provided for download.

---

## 🛠 Technologies Used

* **Python** – Core programming language
* **Flask** – Backend web framework
* **PyCA Cryptography** – AES encryption engine
* **HTML, CSS, JavaScript** – User interface
* **VS Code** – Development workspace

---

## 🔐 Security Highlights

* AES-256 symmetric encryption
* PBKDF2 for generating strong keys from passwords
* Randomized salt and IV for each encryption
* PKCS7 padding for consistent data structure
* Secure temporary data handling

---

## 📁 Functional Capabilities

* Upload and preview images in real time
* Encrypt/decrypt without storing images on the server
* Automatic download system for output files
* Clean error messages and validation checks
* Smooth transitions and responsive layout

---

## 🧩 Architecture Overview

* **UI Layer:** Handles input, previews, and user interactions.
* **Flask Backend:** Routes requests and manages cryptographic operations.
* **Encryption Engine:** Performs AES-256, padding, salt & IV management.
* **File Handler:** Generates encrypted/decrypted outputs securely.

---

## 🚧 Challenges & Solutions

| Issue                        | Resolution                                    |
| ---------------------------- | --------------------------------------------- |
| Preview inconsistencies      | Improved finalization steps and file handling |
| File download failures       | Split routes for processing and downloading   |
| UI performance dips          | Optimized JavaScript and styling logic        |
| Maintaining crypto integrity | Strengthened AES implementation               |

---

## ✔️ Project Outcomes

* Created a fully operational image encryption platform
* Achieved consistent and secure cryptographic processing
* Delivered a polished and user-friendly interface
* Ensured the system aligns with modern cybersecurity standards

---

## 🌟 Future Improvements

* Multi-user login system
* Encrypted cloud storage support
* Additional encryption modes
* Batch processing for multiple images
* Activity logging and audit trail
* Complete mobile optimization

---

## 🏁 Conclusion

This web application presents a practical and secure solution for protecting image files using strong encryption techniques. It blends cybersecurity principles with a clean interface, making encryption accessible for both technical and non-technical users. The project highlights how cryptography can be applied effectively in real-world digital protection scenarios.

