import jwt from "jsonwebtoken";
import dotenv from "dotenv";
dotenv.config();
const JWT_SECRET = process.env.JWT_SECRET || "CHANGE_THIS";

export function generateToken(user) {
  const payload = { id: user._id || user.id || null, role: user.role || user.role, username: user.username || user.username, patientId: user.patientId || null };
  return jwt.sign(payload, JWT_SECRET, { expiresIn: "2h" });
}

export function verifyToken(token) {
  return jwt.verify(token, JWT_SECRET);
}
