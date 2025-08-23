const jwt = require('jsonwebtoken');

export default async function handler(req, res) {
  // Handle CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    // Get environment variables
    const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'APITMKfqYVjk79h';
    const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA';
    const LIVEKIT_URL = process.env.LIVEKIT_URL || 'wss://sr-fa31r2za.livekit.cloud';

    // Parse query parameters
    const { identity, room } = req.query;
    const participantIdentity = identity || `user_${Date.now()}`;
    const roomName = room || `alex-private-${participantIdentity}`;

    // Create JWT token
    const payload = {
      iss: LIVEKIT_API_KEY,
      sub: participantIdentity,
      name: participantIdentity,
      video: {
        room: roomName,
        roomJoin: true,
        canPublish: true,
        canSubscribe: true,
        canPublishData: true,
      },
      exp: Math.floor(Date.now() / 1000) + (6 * 60 * 60), // 6 hours
    };

    const token = jwt.sign(payload, LIVEKIT_API_SECRET);

    res.status(200).json({
      token: token,
      url: LIVEKIT_URL,
      room: roomName,
      identity: participantIdentity,
    });
  } catch (error) {
    console.error('Error generating token:', error);
    res.status(500).json({ error: 'Failed to generate token' });
  }
}