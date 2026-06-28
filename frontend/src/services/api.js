const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

async function request(path, options) {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    throw new Error(`API request failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export const api = {
  async getMeetings() {
    return request('/api/meetings/?rm_id=rm_sara_001');
  },

  async getCustomers(query = '') {
    return request(`/api/customers/?rm_id=rm_sara_001&query=${encodeURIComponent(query)}`);
  },

  async getAlerts(customerId = 'cust_khaled_001') {
    return request(`/api/alerts/${customerId}`);
  },

  async getActiveCustomer() {
    return request('/api/customers/cust_khaled_001');
  },

  async sendChatMessage(message, history, customerId = 'cust_khaled_001') {
    const data = await request('/api/chat/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        customer_id: customerId,
        rm_id: 'rm_sara_001',
        history,
      }),
    });
    return data.reply;
  },

  async pushToCRM(fields) {
    const values = Array.isArray(fields)
      ? Object.fromEntries(fields.map((field) => [field.label, field.value]))
      : fields;

    return request('/api/crm/update', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_id: 'cust_khaled_001',
        rm_id: 'rm_sara_001',
        topic: values.Topic ?? 'Credit line + FX hedging',
        outcome: values.Outcome ?? 'Positive - follow up',
        action_items: [values['Action item'] ?? 'Send FX sheet by Jun 29'],
        next_steps: values['Next step'] ?? 'Trade finance review',
      }),
    });
  },

  async sendEmail(draft) {
    return request('/api/email/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customer_id: 'cust_khaled_001', rm_id: 'rm_sara_001', draft }),
    });
  },

  async prepareMeetingBrief(customerName, topic) {
    return request('/api/meetings/brief', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ customerName, topic }),
    });
  },
};
