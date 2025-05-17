import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const ListenerDashboard: React.FC = () => {
    const { account } = useAuth();

    return (
        <div className="min-h-screen bg-gray-100 p-4">
            <div className="max-w-4xl mx-auto">
                <div className="bg-white p-4 rounded-lg shadow-md mb-4">
                    <p className="text-sm text-gray-600">Compte auditeur :</p>
                    <p className="font-mono text-sm">{account}</p>
                </div>
                
                <div className="bg-white p-6 rounded-lg shadow-md">
                    <h1 className="text-2xl font-bold mb-6">Tableau de bord Auditeur</h1>
                    
                    <div className="mb-8">
                        <h2 className="text-xl font-semibold mb-4">Campagnes disponibles</h2>
                        <div className="space-y-4">
                            {/* Liste des campagnes à implémenter */}
                            <p className="text-gray-500 text-center py-4">
                                Aucune campagne disponible pour le moment
                            </p>
                        </div>
                    </div>
                    
                    <div>
                        <h2 className="text-xl font-semibold mb-4">Mes gains</h2>
                        <div className="bg-gray-50 p-4 rounded-lg">
                            <div className="flex justify-between items-center">
                                <div>
                                    <p className="text-sm text-gray-600">Total gagné</p>
                                    <p className="text-2xl font-bold">0.00 XRP</p>
                                </div>
                                <div>
                                    <p className="text-sm text-gray-600">Temps d'écoute</p>
                                    <p className="text-2xl font-bold">0 min</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ListenerDashboard; 