// frontend/src/components/Payments/ConfigureSoundboxModal.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '../ui/dialog';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../ui/select';
import { Settings } from 'lucide-react';

const API = process.env.REACT_APP_API_URL || 'http://localhost:8002';

const ConfigureSoundboxModal = ({ isOpen, onClose, onSave }) => {
  const [loading, setLoading] = useState(false);
  const [config, setConfig] = useState({
    provider: 'paytm',
    merchant_upi_id: '',
    merchant_name: '',
    api_key: '',
    api_secret: ''
  });

  useEffect(() => {
    if (isOpen) {
      fetchExistingConfig();
    }
  }, [isOpen]);

  const fetchExistingConfig = async () => {
    try {
      const response = await axios.get(`${API}/soundbox/config`);
      if (response.data) {
        setConfig({
          provider: response.data.provider || 'paytm',
          merchant_upi_id: response.data.merchant_upi_id || '',
          merchant_name: response.data.merchant_name || '',
          api_key: response.data.api_key || '',
          api_secret: response.data.api_secret || ''
        });
      }
    } catch (error) {
      console.error('Error fetching soundbox config:', error);
    }
  };

  const handleSave = async () => {
    if (!config.merchant_upi_id || !config.merchant_name) {
      alert('Please fill in Merchant UPI ID and Merchant Name');
      return;
    }

    setLoading(true);
    try {
      await axios.post(`${API}/api/soundbox/config`, config);
      alert('✅ Soundbox configured successfully!');
      onSave();
      onClose();
    } catch (error) {
      console.error('Error saving soundbox config:', error);
      alert('❌ Error saving configuration: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Settings className="h-5 w-5 text-orange-600" />
            Configure Soundbox
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4 py-4">
          {/* Provider Selection */}
          <div>
            <Label htmlFor="provider">Soundbox Provider *</Label>
            <Select
              value={config.provider}
              onValueChange={(value) => setConfig({ ...config, provider: value })}
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="paytm">Paytm Soundbox</SelectItem>
                <SelectItem value="phonepe">PhonePe Soundbox</SelectItem>
                <SelectItem value="gpay">Google Pay Soundbox</SelectItem>
                <SelectItem value="other">Other</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Merchant UPI ID */}
          <div>
            <Label htmlFor="merchant_upi_id">Merchant UPI ID *</Label>
            <Input
              id="merchant_upi_id"
              value={config.merchant_upi_id}
              onChange={(e) => setConfig({ ...config, merchant_upi_id: e.target.value })}
              placeholder="e.g., csbcafe@paytm"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Your UPI ID where customers will send payments
            </p>
          </div>

          {/* Merchant Name */}
          <div>
            <Label htmlFor="merchant_name">Merchant Name *</Label>
            <Input
              id="merchant_name"
              value={config.merchant_name}
              onChange={(e) => setConfig({ ...config, merchant_name: e.target.value })}
              placeholder="e.g., CSB Cafe"
              required
            />
            <p className="text-xs text-gray-500 mt-1">
              Name displayed on customer's UPI app
            </p>
          </div>

          {/* API Key */}
          <div>
            <Label htmlFor="api_key">API Key (Optional)</Label>
            <Input
              id="api_key"
              type="password"
              value={config.api_key}
              onChange={(e) => setConfig({ ...config, api_key: e.target.value })}
              placeholder="Enter API key from soundbox provider"
            />
          </div>

          {/* API Secret */}
          <div>
            <Label htmlFor="api_secret">API Secret (Optional)</Label>
            <Input
              id="api_secret"
              type="password"
              value={config.api_secret}
              onChange={(e) => setConfig({ ...config, api_secret: e.target.value })}
              placeholder="Enter API secret from soundbox provider"
            />
          </div>

          {/* Webhook URL Info */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h4 className="font-semibold text-sm text-blue-900 mb-2">
              Webhook Configuration
            </h4>
            <p className="text-xs text-blue-700 mb-2">
              Configure this webhook URL in your {config.provider} merchant dashboard:
            </p>
            <code className="bg-white px-3 py-2 rounded border text-xs block overflow-x-auto">
              {API}/api/webhook/soundbox
            </code>
            <p className="text-xs text-blue-600 mt-2">
              📌 Path: Developer Settings → API Keys → Configure Webhook URL
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-end space-x-2 pt-4 border-t">
          <Button variant="outline" onClick={onClose} disabled={loading}>
            Cancel
          </Button>
          <Button
            onClick={handleSave}
            disabled={loading}
            className="bg-orange-600 hover:bg-orange-700"
          >
            {loading ? 'Saving...' : 'Save Configuration'}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default ConfigureSoundboxModal;
