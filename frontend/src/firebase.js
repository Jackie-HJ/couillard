// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDnNUQRFVb5q4p_LMLMdwrnfaoIsXFVAro",
  authDomain: "blue-ridge-library.firebaseapp.com",
  projectId: "blue-ridge-library",
  storageBucket: "blue-ridge-library.appspot.com",
  messagingSenderId: "338055850934",
  appId: "1:338055850934:web:3bfa59022b5e2c912def17",
  measurementId: "G-GB7ZP35T0J"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);