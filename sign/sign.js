const keccak256 = require('js-sha3').keccak256;
const messages = require('./models_pb');
const secp256k1 = require('secp256k1');
const fs = require('fs');
const path = require('path');

function isHexPrefixed(str) {
  return str.slice(0, 2) === '0x'
}

function stripHexPrefix(str) {
  if (typeof str !== 'string') {
    return str
  }
  return isHexPrefixed(str) ? str.slice(2) : str
}

function toHexString(byteArray, withPrefix) {
  return (
    (withPrefix ? '0x' : '') +
    Array.from(byteArray, function (byte) {
      // eslint-disable-next-line no-bitwise
      return `0${(byte & 0xff).toString(16)}`.slice(-2)
    }).join('')
  )
}

function intToHex(integer) {
  if (integer < 0) {
    throw new Error('Invalid integer as argument, must be unsigned!');
  }
  var hex = integer.toString(16);
  return hex.length % 2 ? '0' + hex : hex;
}

function padToEven(a) {
  return a.length % 2 ? '0' + a : a;
}

function bufferToInt(buf) {
  if (!buf || !buf.length) {
    return 0;
  }
  return parseInt(Buffer.from(buf).toString('hex'), 16);
}

function intToBuffer(integer) {
  var hex = intToHex(integer);
  return Buffer.from(hex, 'hex');
}

function toBuffer(v) {
  if (!Buffer.isBuffer(v)) {
    if (typeof v === 'string') {
      if (isHexPrefixed(v)) {
        return Buffer.from(padToEven(stripHexPrefix(v)), 'hex');
      } else {
        return Buffer.from(v);
      }
    } else if (typeof v === 'number') {
      if (!v) {
        return Buffer.from([]);
      } else {
        return intToBuffer(v);
      }
    } else if (v === null || v === undefined) {
      return Buffer.from([]);
    } else if (v instanceof Uint8Array) {
      return Buffer.from(v);
    } else {
      throw new Error('invalid type');
    }
  }
  return v;
}

function hexToUint8Array(hexString) {
  const str = stripHexPrefix(hexString);

  var arrayBuffer = new Uint8Array(str.length / 2);

  for (var i = 0; i < str.length; i += 2) {
    var byteValue = parseInt(str.substr(i, 2), 16);
    if (isNaN(byteValue)) {
      throw 'Invalid hexString';
    }
    arrayBuffer[i / 2] = byteValue;
  }

  return arrayBuffer;
}

Transaction = class {
  constructor(nonce, epoch, type, to, amount, maxFee, tips, payload, signature) {
    this.nonce = nonce || 0;
    this.epoch = epoch || 0;
    this.type = type || 0;
    this.to = to;
    this.amount = amount || 0;
    this.maxFee = maxFee || 0;
    this.tips = tips || 0;
    this.payload = payload || '0x';
    this.signature = signature || null;
  }
  toJson() {

    var obj = {
      nonce: this.nonce,
      epoch: this.epoch,
      type: this.type,
      to: this.to,
      amount: this.amount,
      maxFee: this.maxFee,
      tips: this.tips,
      payload: this.payload,
      signature: this.signature
    }
    return JSON.stringify(obj);

  }
  fromHex(hex) {
    return this.fromBytes(hexToUint8Array(hex));
  }

  fromBytes(bytes) {
    const protoTx = messages.ProtoTransaction.deserializeBinary(bytes);

    const protoTxData = protoTx.getData();
    this.nonce = protoTxData.getNonce();
    this.epoch = protoTxData.getEpoch();
    this.type = protoTxData.getType();
    this.to = toHexString(protoTxData.getTo(), true);
    this.amount = bufferToInt(protoTxData.getAmount());
    this.maxFee = bufferToInt(protoTxData.getMaxfee());
    this.tips = bufferToInt(protoTxData.getTips());
    this.payload = protoTxData.getPayload();

    this.signature = protoTx.getSignature();

    return this;
  }

  sign(key) {
    const hash = keccak256.array(
      this._createProtoTxData().serializeBinary()
    );
    const {
      signature,
      recid
    } = secp256k1.ecdsaSign(
      new Uint8Array(hash),
      hexToUint8Array(key)
    );

    this.signature = Buffer.from([...signature, recid]);

    return this;
  }

  toBytes() {
    const transaction = new messages.ProtoTransaction();
    transaction.setData(this._createProtoTxData());
    if (this.signature) {
      transaction.setSignature(toBuffer(this.signature));
    }
    return Buffer.from(transaction.serializeBinary());
  }

  toHex() {
    return this.toBytes().toString('hex');
  }

  _createProtoTxData() {
    const data = new messages.ProtoTransaction.Data();
    data.setNonce(this.nonce).setEpoch(this.epoch).setType(this.type);

    if (this.to) {
      data.setTo(toBuffer(this.to));
    }

    if (this.amount) {
      data.setAmount(toBuffer(this.amount));
    }
    if (this.maxFee) {
      data.setMaxfee(toBuffer(this.maxFee));
    }
    if (this.amount) {
      data.setTips(toBuffer(this.tips));
    }
    if (this.payload) {
      data.setPayload(toBuffer(this.payload));
    }

    return data;
  }
}

const tx = process.argv.slice(2)[0];
const currentScriptDirectory = __dirname;
const jsonFilePath = path.join(currentScriptDirectory, '..', "config.json");

fs.readFile(jsonFilePath, 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading JSON file:', err);
        return;
    }

    try {
        const jsonData = JSON.parse(data);
        const key = jsonData.private_key;
        console.log('0x' + new Transaction().fromHex(tx).sign(key).toHex())
    } catch (jsonParseError) {
        console.error('Error parsing JSON:', jsonParseError);
    }
});