from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Util.Padding import unpad
import base64

# 假设数据库地址的密文（base64 编码）
encrypted_db_address = "IxfjWn75P2gxl3icEwGWcciEYGNTqn+GSXaSQ180Swk="  # 这里填入你实际的密文（应该是 base64 编码的）

# 盐值
salt = b"aB3hF7zK9tL2pQ0X"

# # 假设的密码（或者你可以替换为你实际的密码）
# password = b"your_password_here"  # 密码或其他密钥

# # 使用 scrypt 生成 AES 密钥（这里使用 scrypt 作为密钥派生函数）
key = scrypt(password, salt, dkLen=32)  # 32 字节的密钥长度适用于 AES-256

# # 解密模式为 CBC，假设初始化向量（IV）已知
# # 如果密文存储的 IV 是前面的一部分，可以提取出来
# iv = b"16_byte_iv_value"  # 需要替换为实际的 IV（16 字节）

# 解码 base64 编码的密文
ciphertext = base64.b64decode(encrypted_db_address)

# 创建 AES 解密器
cipher = AES.new(key, AES.MODE_CBC, iv)

# 解密并去除填充
decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

# 将解密后的数据转换为字符串（假设是 UTF-8 编码的）
decrypted_db_address = decrypted_data.decode('utf-8')

# 输出解密后的数据库地址
print(f"解密后的数据库地址: {decrypted_db_address}")
