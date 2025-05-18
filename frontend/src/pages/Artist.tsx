import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { CampaignService, Campaign } from '../services/campaign.service';

const ArtistDashboard: React.FC = () => {
    const { account } = useAuth();
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    
    // Form state
    const [songTitle, setSongTitle] = useState('');
    const [songUrl, setSongUrl] = useState('');
    const [amount, setAmount] = useState('20');

    useEffect(() => {
        loadCampaigns();
    }, []);

    const loadCampaigns = async () => {
        try {
            const data = await CampaignService.getActiveCampaigns();
            setCampaigns(data);
        } catch (err) {
            console.error('Erreur lors du chargement des campagnes:', err);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);
        setIsLoading(true);

        try {
            if (!account) {
                throw new Error('Vous devez être connecté pour créer une campagne');
            }

            await CampaignService.createCampaign({
                artistAddress: account,
                songTitle,
                songUrl,
                amount: parseFloat(amount)
            });

            // Réinitialiser le formulaire
            setSongTitle('');
            setSongUrl('');
            setAmount('20');

            // Recharger les campagnes
            await loadCampaigns();
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Une erreur est survenue');
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async (campaignId: number) => {
        if (!account) return;
        
        if (!window.confirm('Êtes-vous sûr de vouloir supprimer cette campagne ?')) {
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            await CampaignService.deleteCampaign(campaignId, account);
            await loadCampaigns();
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Une erreur est survenue');
        } finally {
            setIsLoading(false);
        }
    };

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
                        {error && (
                            <div className="bg-red-50 text-red-600 p-4 rounded-lg mb-4">
                                {error}
                            </div>
                        )}
                        <form onSubmit={handleSubmit} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">
                                    Titre de la chanson
                                </label>
                                <input
                                    type="text"
                                    value={songTitle}
                                    onChange={(e) => setSongTitle(e.target.value)}
                                    required
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            
                            <div>
                                <label className="block text-sm font-medium text-gray-700">
                                    URL de la chanson
                                </label>
                                <input
                                    type="url"
                                    value={songUrl}
                                    onChange={(e) => setSongUrl(e.target.value)}
                                    required
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
                                    value={amount}
                                    onChange={(e) => setAmount(e.target.value)}
                                    required
                                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                                />
                            </div>
                            
                            <button
                                type="submit"
                                disabled={isLoading}
                                className="w-full bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
                            >
                                {isLoading ? 'Création en cours...' : 'Créer la campagne'}
                            </button>
                        </form>
                    </div>
                    
                    <div>
                        <h2 className="text-xl font-semibold mb-4">Mes campagnes</h2>
                        <div className="space-y-4">
                            {campaigns.length === 0 ? (
                                <p className="text-gray-500 text-center py-4">
                                    Aucune campagne active pour le moment
                                </p>
                            ) : (
                                campaigns.map((campaign) => (
                                    <div 
                                        key={campaign.id}
                                        className="bg-gray-50 p-4 rounded-lg"
                                    >
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <h3 className="font-semibold">{campaign.song_title}</h3>
                                                <div className="mt-2 space-y-1">
                                                    <p className="text-sm text-gray-600">
                                                        Montant total : {campaign.total_amount} XRP
                                                    </p>
                                                    <p className="text-sm text-gray-600">
                                                        Restant : {campaign.remaining_amount} XRP
                                                    </p>
                                                    <p className="text-sm text-gray-600">
                                                        Paiement par seconde : {campaign.amount_per_second} XRP
                                                    </p>
                                                </div>
                                            </div>
                                            {campaign.artist_address === account && (
                                                <button
                                                    onClick={() => handleDelete(campaign.id)}
                                                    disabled={isLoading}
                                                    className="text-red-600 hover:text-red-800 disabled:opacity-50"
                                                >
                                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                                        <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                                                    </svg>
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ArtistDashboard; 