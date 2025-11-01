import crypto from "crypto";
import dotenv from "dotenv";
dotenv.config();

const ALGO = "aes-256-cbc";
const SECRET_KEY = process.env.AES_SECRET_KEY;
const IV_LENGTH = parseInt(process.env.AES_IV_LENGTH || "16", 10);

if (!SECRET_KEY || SECRET_KEY.length !== 32) {
  console.warn("AES_SECRET_KEY should be 32 characters for AES-256. Check .env.");
}

export function encryptData(plainText) {
  const iv = crypto.randomBytes(IV_LENGTH);
  const cipher = crypto.createCipheriv(ALGO, Buffer.from(SECRET_KEY), iv);
  let encrypted = cipher.update(plainText, "utf8", "hex");
  encrypted += cipher.final("hex");
  return {
    iv: iv.toString("hex"),
    data: encrypted
  };
}

export function decryptData(encryptedHex, ivHex) {
  const iv = Buffer.from(ivHex, "hex");
  const decipher = crypto.createDecipheriv(ALGO, Buffer.from(SECRET_KEY), iv);
  let decrypted = decipher.update(encryptedHex, "hex", "utf8");
  decrypted += decipher.final("utf8");
  return decrypted;
}

export function encryptForDB(plainText) {
  const { iv, data } = encryptData(plainText);
  return `${iv}:${data}`;
}

export function decryptFromDB(stored) {
  if (!stored) return null;
  const [iv, data] = stored.split(":");
  if (!iv || !data) return null;
  return decryptData(data, iv);
}

// Fingerprint indexing (SHA256) - create a one-way index for 1:N lookup
export function fingerprintIndex(templateBase64) {
  if (!templateBase64) return null;
  const hash = crypto.createHash('sha256');
  hash.update(templateBase64);
  return hash.digest('hex'); // store this in patient.fingerprint_index
}
