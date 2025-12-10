// Public key for RSA encryption - must match the backend's public.key in application.properties
const publicKeyPEM = `
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArkOuYMSFFatZA+PhgW6cVMVBPBdePouwHMsZYmY1vndJLQcSPzsJywdB+N5uncfgZWhTKu7ByQy/DZnpRFiMpntUCLD2c0eOZH8rqzbT+eDtemKVSmFVfz8cuWcqPJz048nqtrnKHwz/IaJvjiyBCj2BWlNgu4EDLVmDbzQJHgqFlRYad1cPf5JM6IBfZSogAO5iVcAmBTa0jz5hGiVE74QhIzes0yNrpH7VOLrVpjJo5J5dUw8iRwDVTWeNat2T+tjeMgzrQjQML2ooPasLzkEy7Jgsh3oJoAs357nKlNRWXkFzR8WUFTv+IH2rr3Hilz7Mm1thizYA2Dp0KRbypwIDAQAB
-----END PUBLIC KEY-----
`;

/**
 * Encrypt a password using RSA public key encryption
 * @param {string} username - The username
 * @param {string} password - The plain text password
 * @returns {object} Object containing username and encrypted password
 */
export function encryptPassword(username, password) {
  try {
    console.log('Starting encryption...')
    
    // Parse the public key
    const pub = KEYUTIL.getKey(publicKeyPEM)
    console.log('Public key parsed successfully')

    // Encrypt using PKCS#1 v1.5 padding (RSA)
    // Using RSAKey.encrypt instead of KJUR.crypto.Cipher.encrypt
    const encryptedHex = KJUR.crypto.Cipher.encrypt(password, pub, 'RSA')
    console.log('Encrypted hex:', encryptedHex)
    
    // Convert hex to base64 for Java backend
    const encryptedBase64 = hextob64(encryptedHex)
    console.log('Encrypted base64:', encryptedBase64)

    return {
      username: username,
      password: encryptedBase64
    }
  } catch (error) {
    console.error('Encryption error details:', error)
    console.error('Error message:', error.message)
    console.error('Error stack:', error.stack)
    throw new Error('Failed to encrypt password')
  }
}

/**
 * Convert string to hex
 * @param {string} str - Input string
 * @returns {string} Hex encoded string
 */
function stringToHex(str) {
  let hex = ''
  for (let i = 0; i < str.length; i++) {
    const charCode = str.charCodeAt(i)
    const hexValue = charCode.toString(16).padStart(2, '0')
    hex += hexValue
  }
  return hex
}

/**
 * Helper function for backward compatibility with hex2b64
 * Now uses jsrsasign's built-in hextob64 function
 */
export function hex2b64(hexString) {
  return hextob64(hexString)
}
 