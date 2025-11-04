import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';
import Dashboard from './components/Dashboard/Dashboard';
import FamousMovies from './components/Movies/FamousMovies';
import CustomAnalysis from './components/Analysis/CustomAnalysis';
import MovieSearch from './components/Movies/MovieSearch';
import Navbar from './components/Layout/Navbar';
import { AuthProvider, useAuth } from './context/AuthContext';

function PrivateRoute({ children }) {
  const { user } = useAuth();
  return user ? children : <Navigate to="/login" />;
}

function AppRoutes() {
  const { user } = useAuth();

  return (
    <Router>
      {user && <Navbar />}
      <Routes>
        <Route path="/login" element={user ? <Navigate to="/dashboard" /> : <Login />} />
        <Route path="/signup" element={user ? <Navigate to="/dashboard" /> : <Signup />} />
        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          }
        />
        <Route
          path="/famous-movies"
          element={
            <PrivateRoute>
              <FamousMovies />
            </PrivateRoute>
          }
        />
        <Route
          path="/custom-analysis"
          element={
            <PrivateRoute>
              <CustomAnalysis />
            </PrivateRoute>
          }
        />
        <Route
          path="/movie-search"
          element={
            <PrivateRoute>
              <MovieSearch />
            </PrivateRoute>
          }
        />
        <Route path="/" element={<Navigate to={user ? "/dashboard" : "/login"} />} />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}

export default App;
