
// ==============================
// IMPORTS & INITIAL SETUP
// ==============================
const express = require("express");
const jwt = require("jsonwebtoken");

const app = express();
app.use(express.json());

// ==============================
// CONFIG
// ==============================
const PORT = 3000;
const SECRET = "mysecretkey";

// ==============================
// IN-MEMORY STORAGE (TEMPORARY)
// ==============================
const users = []; // stores registered users
const doctorProfiles = []; // stores doctor profiles
const patientProfiles = []; // stores patient profiles

// ==============================
// ROOT ROUTE (Health Check)
// ==============================
app.get("/", (req, res) => {
  res.send("Server is running");
});

// ==============================
// AUTH ROUTES
// ==============================

// Signup API (Doctor / Patient)
app.post("/signup", (req, res) => {
  const { email, password, role } = req.body;

  // Validate input
  if (!email || !password || !role) {
    return res.status(400).json({ message: "All fields are required" });
  }

  // Validate role
  if (role !== "doctor" && role !== "patient") {
    return res.status(400).json({ message: "Invalid role" });
  }

  // Check if user already exists
  const existingUser = users.find(user => user.email === email);
  if (existingUser) {
    return res.status(400).json({ message: "User already exists" });
  }

  // Store user
  users.push({ email, password, role });

  res.json({ message: "User registered successfully" });
});

// Login API (Generates JWT Token)
app.post("/login", (req, res) => {
  const { email, password } = req.body;

  // Find user
  const user = users.find(
    u => u.email === email && u.password === password
  );

  if (!user) {
    return res.status(401).json({ message: "Invalid credentials" });
  }

  // Generate JWT token
  const token = jwt.sign(
    { email: user.email, role: user.role },
    SECRET
  );

  res.json({ message: "Login successful", token });
});

// ==============================
// AUTH MIDDLEWARE
// ==============================
function authMiddleware(req, res, next) {
  const token = req.headers.authorization;

  // Check token presence
  if (!token) {
    return res.status(401).json({ message: "No token provided" });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, SECRET);
    req.user = decoded; // attach user data to request
    next();
  } catch (err) {
    return res.status(401).json({ message: "Invalid token" });
  }
}

// ==============================
// PROTECTED TEST ROUTES
// ==============================

// Doctor-only route
app.get("/doctor", authMiddleware, (req, res) => {
  if (req.user.role !== "doctor") {
    return res.status(403).json({ message: "Access denied" });
  }

  res.json({ message: "Welcome Doctor" });
});

// Patient-only route
app.get("/patient", authMiddleware, (req, res) => {
  if (req.user.role !== "patient") {
    return res.status(403).json({ message: "Access denied" });
  }

  res.json({ message: "Welcome Patient" });
});

// ==============================
// DOCTOR ONBOARDING
// ==============================
app.post("/doctor/profile", authMiddleware, (req, res) => {
  if (req.user.role !== "doctor") {
    return res.status(403).json({ message: "Access denied" });
  }

  const { name, specialization } = req.body;

  // Check if profile already exists
  const existing = doctorProfiles.find(
    d => d.email === req.user.email
  );

  if (existing) {
    existing.name = name;
    existing.specialization = specialization;

    return res.json({
      message: "Doctor profile updated",
      profile: existing
    });
  }

  // Create new profile
  const newProfile = {
    email: req.user.email,
    name,
    specialization
  };

  doctorProfiles.push(newProfile);

  res.json({
    message: "Doctor profile created",
    profile: newProfile
  });
});

// ==============================
// PATIENT ONBOARDING
// ==============================
app.post("/patient/profile", authMiddleware, (req, res) => {
  if (req.user.role !== "patient") {
    return res.status(403).json({ message: "Access denied" });
  }

  const { name, age } = req.body;

  // Check if profile already exists
  const existing = patientProfiles.find(
    p => p.email === req.user.email
  );

  if (existing) {
    existing.name = name;
    existing.age = age;

    return res.json({
      message: "Patient profile updated",
      profile: existing
    });
  }

  // Create new profile
  const newProfile = {
    email: req.user.email,
    name,
    age
  };

  patientProfiles.push(newProfile);

  res.json({
    message: "Patient profile created",
    profile: newProfile
  });
});

// ==============================
// DOCTOR DISCOVERY API
// ==============================
app.get("/doctors", (req, res) => {
  const { specialization } = req.query;

  // Filter by specialization if provided
  if (specialization) {
    const filteredDoctors = doctorProfiles.filter(
      d => d.specialization === specialization
    );
    return res.json(filteredDoctors);
  }

  // Return all doctors
  res.json(doctorProfiles);
});

// ==============================
// START SERVER
// ==============================
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});