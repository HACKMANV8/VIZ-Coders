import mongoose from 'mongoose';

const PatientSchema = new mongoose.Schema({
  patientId: { type: String, unique: true, required: true },
  name_encrypted: { type: String },
  dob_encrypted: { type: String },
  aadhaar_encrypted: { type: String },
  healthCard_encrypted: { type: String },
  fingerprint_encrypted: { type: String },
  fingerprint_index: { type: String },
  medicalHistory_encrypted: { type: String },
  createdAt: { type: Date, default: Date.now }
});

export default mongoose.model('Patient', PatientSchema);
