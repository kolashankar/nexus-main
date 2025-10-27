/**
 * Main App component
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import useStore from './store';
import Header from './components/layout/Header/Header';
import Footer from './components/layout/Footer/Footer';
import Landing from './pages/Landing/Landing';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import Play from './pages/Play/Play';
import Combat from './pages/Combat/Combat';
import { Actions } from './pages/Actions/Actions';
import Guild from './pages/Guild/Guild';
import { Karma } from './pages/Karma/Karma';
import Prestige from './pages/Prestige/Prestige';
import Profile from './pages/Profile/Profile';
import { Progression } from './pages/Progression/Progression';
import { QuestsDashboard as Quests } from './pages/Quests/QuestsDashboard';
import Seasonal from './pages/Seasonal/SeasonalDashboard';
import { Skills } from './pages/Skills/Skills';
import SocialHub from './pages/SocialHub/SocialHub';
import Territories from './pages/Territories/Territories';
import World from './pages/World/WorldDashboard';
import { Toaster } from './components/ui/sonner';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  return <>{children}</>;
};

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/play"
              element={
                <ProtectedRoute>
                  <Play />
                </ProtectedRoute>
              }
            />
            <Route
              path="/combat"
              element={
                <ProtectedRoute>
                  <Combat />
                </ProtectedRoute>
              }
            />
            <Route
              path="/actions"
              element={
                <ProtectedRoute>
                  <Actions />
                </ProtectedRoute>
              }
            />
            <Route
              path="/guild"
              element={
                <ProtectedRoute>
                  <Guild />
                </ProtectedRoute>
              }
            />
            <Route
              path="/karma"
              element={
                <ProtectedRoute>
                  <Karma />
                </ProtectedRoute>
              }
            />
            <Route
              path="/prestige"
              element={
                <ProtectedRoute>
                  <Prestige />
                </ProtectedRoute>
              }
            />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/progression"
              element={
                <ProtectedRoute>
                  <Progression />
                </ProtectedRoute>
              }
            />
            <Route
              path="/quests"
              element={
                <ProtectedRoute>
                  <Quests />
                </ProtectedRoute>
              }
            />
            <Route
              path="/seasonal"
              element={
                <ProtectedRoute>
                  <Seasonal />
                </ProtectedRoute>
              }
            />
            <Route
              path="/skills"
              element={
                <ProtectedRoute>
                  <Skills />
                </ProtectedRoute>
              }
            />
            <Route
              path="/social"
              element={
                <ProtectedRoute>
                  <SocialHub />
                </ProtectedRoute>
              }
            />
            <Route
              path="/territories"
              element={
                <ProtectedRoute>
                  <Territories />
                </ProtectedRoute>
              }
            />
            <Route
              path="/world"
              element={
                <ProtectedRoute>
                  <World />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
        <Footer />
        <Toaster />
      </div>
    </BrowserRouter>
  );
}

export default App;