import React from 'react';
import { useAuth } from '@/hooks/useAuth';
import UpgradeStationMain from '@/components/upgrades/UpgradeStation/UpgradeStation';
import { Navigate } from 'react-router-dom';

/**
 * UpgradeStation Page Wrapper
 * Full page component for the upgrade station
 */
const UpgradeStation = () => {
  const { user } = useAuth();

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900">
      <div className="container mx-auto px-4 py-8">
        <UpgradeStationMain />
      </div>
    </div>
  );
};

export default UpgradeStation;