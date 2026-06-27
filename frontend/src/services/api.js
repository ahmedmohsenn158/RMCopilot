const delay = (ms) => new Promise((res) => setTimeout(res, ms));

export const api = {
  async getMeetings() {
    await delay(300);
    const { meetings } = await import('../utils/mockData.js');
    return meetings;
  },

  async getCustomers(query = '') {
    await delay(200);
    const { customers } = await import('../utils/mockData.js');
    if (!query) return customers;
    return customers.filter(
      (c) =>
        c.name.toLowerCase().includes(query.toLowerCase()) ||
        c.segment.toLowerCase().includes(query.toLowerCase()) ||
        c.accountNo.includes(query)
    );
  },

  async getAlerts(customerId) {
    await delay(250);
    const { alerts } = await import('../utils/mockData.js');
    return alerts;
  },

  async getActiveCustomer() {
    await delay(200);
    const { activeCustomer } = await import('../utils/mockData.js');
    return activeCustomer;
  },

  async sendChatMessage(message, history) {
    await delay(800);
    // Mock responses keyed to common queries
    const lowerMsg = message.toLowerCase();
    if (lowerMsg.includes('fx') || lowerMsg.includes('forward')) {
      return "Here's a tailored FX Forward Contract pitch for Khaled:\n\n*'Given your recent USD import activity, our 3-month forward contract lets you lock in today's rate of 30.85 EGP/USD. On a USD 500K exposure, a 2% rate move could cost you EGP 308K — the forward eliminates that risk entirely for a small premium.'*\n\nShall I prepare the full product sheet and pricing?";
    }
    if (lowerMsg.includes('trade finance') || lowerMsg.includes('renewal')) {
      return "Trade finance renewal process:\n\n1. RM submits renewal request via the Trade portal (3 working days before expiry)\n2. Credit team reviews — standard SLA is 5 business days\n3. Customer signs updated facility letter\n4. Limit reinstated automatically on signature date\n\nFor Khaled, the deadline to initiate is **June 28**. Want me to draft the internal request?";
    }
    if (lowerMsg.includes('blocked card') || lowerMsg.includes('angry')) {
      return "Blocked card de-escalation script:\n\n*'I completely understand your frustration, and I sincerely apologise for the inconvenience. Let me pull up your account right now. [pause] I can see the block was triggered by our security system — I'm going to connect you with our cards team who can restore access immediately while we're on the call. Can I place you on a brief hold for 2 minutes?'*\n\nKey: never promise a timeline you can't control. Offer the transfer immediately.";
    }
    if (lowerMsg.includes('new') || lowerMsg.includes('onboard') || lowerMsg.includes('first call')) {
      return "Before your first client call, here's what to do:\n\n1. **Read the 360 profile** — check balance, products, last interaction, open alerts\n2. **Check for pending actions** — any follow-ups from previous RMs?\n3. **Scan the alert panel** — know about any issues before the customer mentions them\n4. **Prep one talking point** — identify one proactive thing you can offer (expiring product, eligibility for upgrade)\n\nThe goal is to sound like you've known them for years, even on day one.";
    }
    return `I've noted your question: "${message}". In a live deployment, I would query the customer database and knowledge base to give you a precise answer. For now, I can see this relates to your client portfolio — would you like me to pull up a specific customer profile or policy document?`;
  },

  async pushToCRM(fields) {
    await delay(600);
    return { success: true, message: 'CRM updated successfully' };
  },

  async sendEmail(draft) {
    await delay(500);
    return { success: true, message: 'Email sent and logged' };
  },

  async prepareMeetingBrief(customerName, topic) {
    await delay(700);
    return {
      success: true,
      brief: `Meeting brief generated for ${customerName} — ${topic}`,
    };
  },
};