import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const ArtistDashboard: React.FC = () => {
    const { account } = useAuth();

    return (
        <div className="min-h-screen bg-gray-100 p-4">
            <div className="max-w-4xl mx-auto">
                <div className="bg-white p-4 rounded-lg shadow-md mb-4">
                    <p className="text-sm text-gray-600">Compte artiste :</p>
                    <p className="font-mono text-sm">{account}</p>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h1 className="text-2xl font-bold mb-6">Tableau de bord Artiste</h1>
                    
                    <div className="mb-8">
                        <h2 className="text-xl font-semibold mb-4">Créer une nouvelle campagne</h2>
                        <form className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">
                                    Titre de la chanson
                                </label>
                                <input
                                    type="text"
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            
                            <div>
                                <label className="block text-sm font-medium text-gray-700">
                                    URL de la chanson
                                </label>
                                <input
                                    type="url"
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            
                            <div>
                                <label className="block text-sm font-medium text-gray-700">
                                    Montant XRP total
                                </label>
                                <input
                                    type="number"
                                    min="20"
                                    step="0.1"
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            
                            <button
                                type="submit"
                                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                            >
                                Créer la campagne
                            </button>
                        </form>
                    </div>
                    
                    <div>
                        <h2 className="text-xl font-semibold mb-4">Mes campagnes</h2>
                        <div className="space-y-4">
                            {/* Liste des campagnes à implémenter */}
                            <p className="text-gray-500 text-center py-4">
                                Aucune campagne active pour le moment
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ArtistDashboard; 