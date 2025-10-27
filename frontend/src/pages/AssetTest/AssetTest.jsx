import React, { useState, useEffect } from 'react';
import { verifyAssets, assetLoader } from '../../utils/assetLoader';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';
import { Button } from '../../components/ui/button';

/**
 * Asset Testing Page
 * Displays all assets and their loading status
 */
const AssetTest = () => {
  const [verification, setVerification] = useState(null);
  const [loading, setLoading] = useState(false);
  const [testResults, setTestResults] = useState({});

  useEffect(() => {
    runVerification();
  }, []);

  const runVerification = async () => {
    setLoading(true);
    const results = await verifyAssets();
    setVerification(results);
    setLoading(false);
  };

  const testAssetCategory = async (category, paths) => {
    setTestResults(prev => ({ ...prev, [category]: { loading: true } }));
    
    const results = await Promise.allSettled(
      paths.map(async (path) => {
        const exists = await assetLoader.checkAsset(path);
        return { path, exists };
      })
    );

    const tested = results
      .filter(r => r.status === 'fulfilled')
      .map(r => r.value);

    setTestResults(prev => ({
      ...prev,
      [category]: {
        loading: false,
        total: paths.length,
        available: tested.filter(t => t.exists).length,
        missing: tested.filter(t => !t.exists).map(t => t.path)
      }
    }));
  };

  const assetCategories = {
    images: [
      '/images/logo.png',
      '/images/logo.svg',
      '/images/placeholder_avatar.png',
      '/images/cyberpunk_city.jpg',
      '/images/hero_background.jpg'
    ],
    icons: [
      '/icons/health.svg',
      '/icons/energy.svg',
      '/icons/karma.svg',
      '/icons/coins.svg',
      '/icons/experience.svg'
    ],
    models: [
      '/models/characters/male_base.glb',
      '/models/characters/female_base.glb',
      '/models/placeholders/character_placeholder.glb',
      '/models/robots/scout.glb',
      '/models/environment/buildings/tower.glb'
    ],
    sounds: [
      '/sounds/menu_click.wav',
      '/sounds/notification.wav',
      '/sounds/level_up.wav',
      '/sounds/combat_hit.wav'
    ],
    fonts: [
      '/fonts/game_font_regular.woff2',
      '/fonts/game_font_bold.woff2'
    ]
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8">
      <div className="max-w-6xl mx-auto">
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-3xl font-bold">Asset Verification Dashboard</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
                <p>Verifying assets...</p>
              </div>
            ) : verification ? (
              <div className="space-y-4">
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-green-100 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-green-800">{verification.available}</div>
                    <div className="text-sm text-green-600">Available</div>
                  </div>
                  <div className="bg-red-100 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-red-800">{verification.missing}</div>
                    <div className="text-sm text-red-600">Missing</div>
                  </div>
                  <div className="bg-blue-100 p-4 rounded-lg">
                    <div className="text-2xl font-bold text-blue-800">{verification.total}</div>
                    <div className="text-sm text-blue-600">Total Checked</div>
                  </div>
                </div>

                {verification.missingPaths && verification.missingPaths.length > 0 && (
                  <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
                    <h3 className="font-bold text-yellow-800 mb-2">Missing Assets:</h3>
                    <ul className="list-disc list-inside text-sm text-yellow-700">
                      {verification.missingPaths.map((path, idx) => (
                        <li key={idx} className="font-mono">{path}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <Button onClick={runVerification} className="w-full">
                  Re-run Verification
                </Button>
              </div>
            ) : null}
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {Object.entries(assetCategories).map(([category, paths]) => (
            <Card key={category}>
              <CardHeader>
                <CardTitle className="capitalize">{category}</CardTitle>
              </CardHeader>
              <CardContent>
                <Button
                  onClick={() => testAssetCategory(category, paths)}
                  disabled={testResults[category]?.loading}
                  className="w-full mb-4"
                >
                  {testResults[category]?.loading ? 'Testing...' : `Test ${category}`}
                </Button>

                {testResults[category] && !testResults[category].loading && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>Available:</span>
                      <span className="font-bold text-green-600">
                        {testResults[category].available}/{testResults[category].total}
                      </span>
                    </div>

                    {testResults[category].missing.length > 0 && (
                      <div className="bg-red-50 p-2 rounded text-xs">
                        <div className="font-bold text-red-800 mb-1">Missing:</div>
                        {testResults[category].missing.map((path, idx) => (
                          <div key={idx} className="text-red-600 font-mono truncate">
                            {path}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                <div className="mt-4 space-y-1">
                  <div className="text-xs font-bold text-gray-600">Sample Paths:</div>
                  {paths.slice(0, 3).map((path, idx) => (
                    <div key={idx} className="text-xs text-gray-500 font-mono truncate">
                      {path}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Visual Asset Preview */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Asset Preview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {/* Images */}
              <div className="space-y-2">
                <div className="text-sm font-bold">Logo</div>
                <img 
                  src="/images/logo.png" 
                  alt="Logo" 
                  className="w-full h-20 object-contain bg-gray-100 rounded"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'block';
                  }}
                />
                <div style={{display: 'none'}} className="text-xs text-red-500">Failed to load</div>
              </div>

              {/* Icons */}
              {['health', 'energy', 'karma', 'coins'].map(icon => (
                <div key={icon} className="space-y-2">
                  <div className="text-sm font-bold capitalize">{icon}</div>
                  <img 
                    src={`/icons/${icon}.svg`}
                    alt={icon}
                    className="w-full h-20 object-contain bg-gray-100 rounded p-2"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'block';
                    }}
                  />
                  <div style={{display: 'none'}} className="text-xs text-red-500">Failed to load</div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AssetTest;
