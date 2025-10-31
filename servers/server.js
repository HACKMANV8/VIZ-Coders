import dotenv from "dotenv";
dotenv.config();

require("dotenv").config();

// ✅ Debug line to verify .env
console.log(" Environment Loaded:", process.env.AES_SECRET_KEY, process.env.MONGO_URI);

const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());

// ✅ Connect to MongoDB
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("✅MongoDB Connected"))
  .catch((err) => console.log("❌ MongoDB connection failed:", err.message));

app.listen(process.env.PORT || 5000, () => {
  console.log(🚀 Server running on port ${process.env.PORT});
});
