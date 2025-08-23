const jwt = require('jsonwebtoken');

exports.handler = async (event, context) => {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
      body: '',
    };
  }

  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    // Get environment variables
    const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || 'APITMKfqYVjk79h';
    const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || 'gCkm5chxksS9KKIUrWVDhf7TDVRVeqleZHf49SFPLBMA';
    const LIVEKIT_URL = process.env.LIVEKIT_URL || 'wss://sr-fa31r2za.livekit.cloud';

    // Parse query parameters
    const queryParams = event.queryStringParameters || {};
    const identity = queryParams.identity || `user_${Date.now()}`;
    const room = queryParams.room || `alex-private-${identity}`;

    // Create JWT token
    const payload = {
      iss: LIVEKIT_API_KEY,
      sub: identity,
      name: identity,
      video: {
        room: room,
        roomJoin: true,
        canPublish: true,
        canSubscribe: true,
        canPublishData: true,
      },
      exp: Math.floor(Date.now() / 1000) + (6 * 60 * 60), // 6 hours
    };

    const token = jwt.sign(payload, LIVEKIT_API_SECRET);

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        token: token,
        url: LIVEKIT_URL,
        room: room,
        identity: identity,
      }),
    };
  } catch (error) {
    console.error('Error generating token:', error);
    return {
      statusCode: 500,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ error: 'Failed to generate token' }),
    };
  }
};