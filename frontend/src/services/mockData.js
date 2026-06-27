export const currentRM = {
  name: 'Sara Hassan',
  role: 'Relationship Manager',
  initials: 'SH',
};

export const stats = [
  { label: 'Total customers', value: 47, color: 'default' },
  { label: 'Pending actions', value: 6, color: 'warning' },
  { label: 'Meetings today', value: 3, color: 'success' },
  { label: 'Active alerts', value: 2, color: 'danger' },
];

export const meetings = [
  {
    id: 1,
    time: '10:00 AM',
    name: 'Khaled Al-Sayed',
    initials: 'KA',
    topic: 'Credit line renewal',
    segment: 'SME Gold',
    color: 'accent',
    status: 'urgent',
  },
  {
    id: 2,
    time: '2:30 PM',
    name: 'Nour Farouk',
    initials: 'NF',
    topic: 'Onboarding review',
    segment: 'Retail Silver',
    color: 'success',
    status: 'normal',
  },
  {
    id: 3,
    time: '4:00 PM',
    name: 'Mohamed Ragab',
    initials: 'MR',
    topic: 'Investment portfolio review',
    segment: 'Corporate',
    color: 'warning',
    status: 'normal',
  },
];

export const customers = [
  {
    id: 1,
    name: 'Khaled Al-Sayed',
    initials: 'KA',
    segment: 'SME Gold',
    accountNo: '#00412',
    color: 'accent',
    status: 'alert',
    statusLabel: 'Alert',
  },
  {
    id: 2,
    name: 'Nour Farouk',
    initials: 'NF',
    segment: 'Retail Silver',
    accountNo: '#00389',
    color: 'success',
    status: 'active',
    statusLabel: 'Active',
  },
  {
    id: 3,
    name: 'Mohamed Ragab',
    initials: 'MR',
    segment: 'Corporate',
    accountNo: '#00278',
    color: 'warning',
    status: 'review',
    statusLabel: 'Review due',
  },
  {
    id: 4,
    name: 'Layla Ibrahim',
    initials: 'LI',
    segment: 'Retail Gold',
    accountNo: '#00331',
    color: 'muted',
    status: 'inactive',
    statusLabel: 'Inactive',
  },
];

export const activeCustomer = {
  name: 'Khaled Al-Sayed',
  initials: 'KA',
  segment: 'SME',
  tier: 'Gold',
  joinedYear: 2019,
  callDuration: '3:42',
  stats: [
    { label: 'Total balance', value: 'EGP 2.4M', color: 'default' },
    { label: 'Credit util.', value: '105%', color: 'danger' },
    { label: 'Active products', value: '4', color: 'default' },
    { label: 'NPS score', value: '72', color: 'warning' },
  ],
  tags: [
    { label: 'Current account', color: 'accent' },
    { label: 'Trade finance', color: 'accent' },
    { label: 'No mortgage', color: 'muted' },
    { label: 'No FX hedging', color: 'muted' },
    { label: 'Credit line expiring Jul 26', color: 'warning' },
  ],
  lastContact: 'May 14 — renewal discussion',
  nextMeeting: 'Jun 30',
};

export const alerts = [
  {
    id: 1,
    type: 'danger',
    icon: 'ti-alert-triangle',
    title: 'Credit limit breach',
    body: 'Utilisation hit 105% on revolving credit line. EGP 42K over limit.',
    time: '2 min ago',
    actionLabel: 'Draft response script',
    actionPrompt: 'Draft a response script for the credit limit breach on Khaled Al-Sayed',
  },
  {
    id: 2,
    type: 'warning',
    icon: 'ti-clock',
    title: 'Product expiry',
    body: 'Trade finance facility expires in 28 days. No renewal initiated yet.',
    time: 'Today',
    actionLabel: null,
  },
  {
    id: 3,
    type: 'info',
    icon: 'ti-trending-up',
    title: 'Cross-sell signal',
    body: '3 large USD inflows detected. May benefit from FX hedging product.',
    time: 'This week',
    actionLabel: 'Expand pitch',
    actionPrompt: 'Generate a full FX hedging pitch tailored to Khaled Al-Sayed import business',
  },
];

export const draftEmail = `Dear Khaled,

Thank you for taking the time to speak today. As discussed, I will arrange for our trade finance team to review the USD 500K facility extension. I will also send across our FX hedging product sheet given your import exposure.

I will follow up by Thursday June 29 with full documentation.

Warm regards,
Sara`;

export const crmFields = [
  { label: 'Topic', value: 'Credit line + FX hedging' },
  { label: 'Outcome', value: 'Positive — follow up', color: 'success' },
  { label: 'Action item', value: 'Send FX sheet by Jun 29' },
  { label: 'Next step', value: 'Trade finance review' },
];

export const initialMessages = [
  {
    id: 1,
    role: 'assistant',
    text: "Hi Sara! I can answer questions about your customers, help you prepare for calls, or guide you through bank processes and products. What do you need?",
  },
  {
    id: 2,
    role: 'user',
    text: 'What products is Khaled eligible for right now?',
  },
  {
    id: 3,
    role: 'assistant',
    text: "Based on Khaled's profile, he's a strong candidate for two products right now:\n\n**1. FX Forward Contract** — he's had 3 large USD inflows this month, suggesting import exposure. Locking in a rate could save him significantly.\n\n**2. Credit line top-up** — his revolving facility is at 105% utilisation. Proactively offering an increase positions you as a partner, not a problem-solver.\n\nWant me to draft a pitch script for either?",
  },
];

export const quickChips = [
  { label: 'Products for Khaled?', prompt: 'What products is Khaled Al-Sayed eligible for?' },
  { label: 'Trade finance renewal process', prompt: 'What is the process for renewing a trade finance facility?' },
  { label: 'Blocked card script', prompt: 'How do I handle an angry customer calling about a blocked card?' },
  { label: 'My open action items', prompt: 'Summarise all open action items for my clients this week' },
  { label: 'New RM onboarding tips', prompt: "I am new — what should I do before my first client call?" },
];