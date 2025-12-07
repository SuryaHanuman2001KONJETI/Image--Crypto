import os
import base64
from flask import Flask, request, send_file
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())


# ---------- ENCRYPT ----------
def encrypt_file(filepath, password, name):
    with open(filepath, "rb") as f:
        data = f.read()

    salt = os.urandom(16)
    iv = os.urandom(16)
    key = derive_key(password, salt)

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    base, ext = os.path.splitext(name)
    output_name = f"{base}_encryption{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    with open(output_path, "wb") as f:
        f.write(salt + iv + encrypted)

    return output_name


# ---------- DECRYPT ----------
def decrypt_file(filepath, password, name):
    with open(filepath, "rb") as f:
        data = f.read()

    salt = data[:16]
    iv = data[16:32]
    encrypted_data = data[32:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain = decryptor.update(encrypted_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded_plain) + unpadder.finalize()

    base, ext = os.path.splitext(name)
    output_name = f"{base}_decryption{ext}"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    with open(output_path, "wb") as f:
        f.write(plain)

    return output_name, output_path


@app.route("/")
def index():
    return render_page()


@app.route("/process", methods=["POST"])
def process():
    file = request.files["file"]
    password = request.form["password"]
    action = request.form["action"]

    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # ✅ ENCRYPT
    if action == "encrypt":
        output_name = encrypt_file(file_path, password, filename)

        return f"""
        <script>
            window.onload = function(){{
                document.getElementById("imgPreview").style.display = "none";
                document.getElementById("fileLabel").innerText = "Choose Image";
                document.getElementById("passInput").value = "";
                window.location.href = "/download/{output_name}";
            }}
        </script>
        """ + render_page()

    # ✅ DECRYPT
    else:
        output_name, output_path = decrypt_file(file_path, password, filename)

        with open(output_path, "rb") as img_file:
            preview = base64.b64encode(img_file.read()).decode()

        return f"""
        <script>
            window.onload = function(){{
                document.getElementById("decryptPreview").src = "data:image/jpeg;base64,{preview}";
                document.getElementById("decryptSection").style.display = "block";
                document.getElementById("fileLabel").innerText = "Choose Image";
                document.getElementById("passInput").value = "";
                window.location.href = "/download/{output_name}";
            }}
        </script>
        """ + render_page()


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)


def render_page():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Image Encryption System</title>
<style>
body{
background:linear-gradient(135deg,#0f2027,#203a43,#2c5364);
font-family:Segoe UI;
display:flex;
justify-content:center;
align-items:center;
height:100vh;
}
.container{
background:rgba(255,255,255,0.1);
backdrop-filter:blur(20px);
padding:30px;
border-radius:20px;
color:white;
width:600px;
text-align:center;
}
.upload-box{
border:2px dashed #fff;
padding:15px;
border-radius:12px;
cursor:pointer;
}
input[type=file]{display:none;}
img{max-width:220px;border-radius:10px;margin-top:10px;}
button{
background:#ff512f;
border:none;
color:white;
padding:10px 15px;
border-radius:12px;
cursor:pointer;
margin-top:10px;
}
#decryptSection{
display:none;
margin-top:20px;
}
</style>

<script>
function showPreview(input){
document.getElementById("fileLabel").innerText=input.files[0].name;
let reader=new FileReader();
reader.onload=function(e){
document.getElementById("imgPreview").src=e.target.result;
document.getElementById("imgPreview").style.display="block";
}
reader.readAsDataURL(input.files[0]);
}
function closePreview(){
document.getElementById("decryptSection").style.display="none";
}
</script>
</head>

<body>
<div class="container">
<h2>🔐 Image Encryption System</h2>

<form method="POST" action="/process" enctype="multipart/form-data">

<label class="upload-box">
<span id="fileLabel">Choose Image</span>
<input type="file" name="file" onchange="showPreview(this)" required>
</label>

<img id="imgPreview" style="display:none;"/>

<br><br>
<input type="password" id="passInput" name="password" placeholder="Enter Password" required>

<br>
<button type="submit" name="action" value="encrypt">Encrypt</button>
<button type="submit" name="action" value="decrypt">Decrypt</button>

</form>

<div id="decryptSection">
<h3>Decrypted Preview</h3>
<img id="decryptPreview">
<br>
<button onclick="closePreview()">❌ Close Preview</button>
</div>

</div>
</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
