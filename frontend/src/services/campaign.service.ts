const API_URL = 'http://localhost:8000/api';

export interface Campaign {
    id: number;
    artist_address: string;
    song_title: string;
    song_url: string;
    total_amount: number;
    amount_per_second: number;
    remaining_amount: number;
    created_at: string;
    status: string;
}

export interface CreateCampaignData {
    artistAddress: string;
    songTitle: string;
    songUrl: string;
    amount: number;
}

export const CampaignService = {
    async deleteCampaign(campaignId: number, artistAddress: string): Promise<void> {
        const response = await fetch(`${API_URL}/campaigns/${campaignId}?artist_address=${artistAddress}`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur lors de la suppression de la campagne');
        }
    },

    async createCampaign(data: CreateCampaignData): Promise<Campaign> {
        const response = await fetch(`${API_URL}/campaigns`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur lors de la création de la campagne');
        }

        return response.json();
    },

    async getActiveCampaigns(): Promise<Campaign[]> {
        const response = await fetch(`${API_URL}/campaigns/active`);

        if (!response.ok) {
            throw new Error('Erreur lors du chargement des campagnes');
        }

        return response.json();
    }
}; 