pragma solidity =0.6.4;
// contracts/interface/IApplication.sol
interface IApplication {
    /**
     * @dev Handle syn package
     */
    function handleSynPackage(
        uint8 channelId,
        bytes calldata msgBytes
    ) external returns (bytes memory responsePayload);
    /**
     * @dev Handle ack package
     */
    function handleAckPackage(uint8 channelId, bytes calldata msgBytes) external;
    /**
     * @dev Handle fail ack package
     */
    function handleFailAckPackage(uint8 channelId, bytes calldata msgBytes) external;
}
// contracts/interface/IBSCValidatorSetV2.sol
interface IBSCValidatorSetV2 {
    function misdemeanor(address validator) external;
    function felony(address validator) external;
    function isCurrentValidator(address validator) external view returns (bool);
    function currentValidatorSetMap(address validator) external view returns (uint256);
    function numOfCabinets() external view returns (uint256);
}
// contracts/interface/ICrossChain.sol
interface ICrossChain {
    /**
     * @dev Send package to BNB Beacon Chain
     */
    function sendSynPackage(uint8 channelId, bytes calldata msgBytes, uint256 relayFee) external;
}
// contracts/interface/ILightClient.sol
interface ILightClient {
    function isHeaderSynced(uint64 height) external view returns (bool);
    function getAppHash(uint64 height) external view returns (bytes32);
    function getSubmitter(uint64 height) external view returns (address payable);
}
// contracts/interface/IParamSubscriber.sol
interface IParamSubscriber {
    function updateParam(string calldata key, bytes calldata value) external;
}
// contracts/interface/IRelayerHub.sol
interface IRelayerHub {
    function isRelayer(address sender) external view returns (bool);
}
// contracts/interface/IRelayerIncentivize.sol
interface IRelayerIncentivize {
    function addReward(
        address payable headerRelayerAddr,
        address payable packageRelayer,
        uint256 amount,
        bool fromSystemReward
    ) external returns (bool);
}
// contracts/interface/ISystemReward.sol
interface ISystemReward {
    function claimRewards(address payable to, uint256 amount) external returns (uint256 actualAmount);
}
// contracts/interface/ITokenHub.sol
interface ITokenHub {
    function getMiniRelayFee() external view returns (uint256);
    function getContractAddrByBEP2Symbol(bytes32 bep2Symbol) external view returns (address);
    function getBep2SymbolByContractAddr(address contractAddr) external view returns (bytes32);
    function bindToken(bytes32 bep2Symbol, address contractAddr, uint256 decimals) external;
    function unbindToken(bytes32 bep2Symbol, address contractAddr) external;
    function transferOut(
        address contractAddr,
        address recipient,
        uint256 amount,
        uint64 expireTime
    ) external payable returns (bool);
    function recoverBCAsset(bytes32 tokenSymbol, address recipient, uint256 amount) external;
    function cancelTokenRecoverLock(bytes32 tokenSymbol, address attacker) external;
    /* solium-disable-next-line */
    function batchTransferOutBNB(
        address[] calldata recipientAddrs,
        uint256[] calldata amounts,
        address[] calldata refundAddrs,
        uint64 expireTime
    ) external payable returns (bool);
    function withdrawStakingBNB(uint256 amount) external returns (bool);
    function cancelTransferIn(address tokenAddress, address attacker) external;
}
// contracts/lib/BytesToTypes.sol
/**
 * @title BytesToTypes
 * Copyright (c) 2016-2020 zpouladzade/Seriality
 * @dev The BytesToTypes contract converts the memory byte arrays to the standard solidity types
 * @author pouladzade@gmail.com
 */
library BytesToTypes {
    function bytesToAddress(uint256 _offst, bytes memory _input) internal pure returns (address _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToBool(uint256 _offst, bytes memory _input) internal pure returns (bool _output) {
        uint8 x;
        assembly {
            x := mload(add(_input, _offst))
        }
        x == 0 ? _output = false : _output = true;
    }
    function getStringSize(uint256 _offst, bytes memory _input) internal pure returns (uint256 size) {
        assembly {
            size := mload(add(_input, _offst))
            let chunk_count := add(div(size, 32), 1) // chunk_count = size/32 + 1
            if gt(mod(size, 32), 0) {
                // if size%32 > 0
                chunk_count := add(chunk_count, 1)
            }
            size := mul(chunk_count, 32) // first 32 bytes reseves for size in strings
        }
    }
    function bytesToString(uint256 _offst, bytes memory _input, bytes memory _output) internal pure {
        uint256 size = 32;
        assembly {
            let chunk_count
            size := mload(add(_input, _offst))
            chunk_count := add(div(size, 32), 1) // chunk_count = size/32 + 1
            if gt(mod(size, 32), 0) { chunk_count := add(chunk_count, 1) } // chunk_count++
            for { let index := 0 } lt(index, chunk_count) { index := add(index, 1) } {
                mstore(add(_output, mul(index, 32)), mload(add(_input, _offst)))
                _offst := sub(_offst, 32) // _offst -= 32
            }
        }
    }
    function bytesToBytes32(uint256 _offst, bytes memory _input, bytes32 _output) internal pure {
        assembly {
            mstore(_output, add(_input, _offst))
            mstore(add(_output, 32), add(add(_input, _offst), 32))
        }
    }
    function bytesToInt8(uint256 _offst, bytes memory _input) internal pure returns (int8 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt16(uint256 _offst, bytes memory _input) internal pure returns (int16 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt24(uint256 _offst, bytes memory _input) internal pure returns (int24 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt32(uint256 _offst, bytes memory _input) internal pure returns (int32 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt40(uint256 _offst, bytes memory _input) internal pure returns (int40 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt48(uint256 _offst, bytes memory _input) internal pure returns (int48 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt56(uint256 _offst, bytes memory _input) internal pure returns (int56 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt64(uint256 _offst, bytes memory _input) internal pure returns (int64 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt72(uint256 _offst, bytes memory _input) internal pure returns (int72 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt80(uint256 _offst, bytes memory _input) internal pure returns (int80 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt88(uint256 _offst, bytes memory _input) internal pure returns (int88 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt96(uint256 _offst, bytes memory _input) internal pure returns (int96 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt104(uint256 _offst, bytes memory _input) internal pure returns (int104 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt112(uint256 _offst, bytes memory _input) internal pure returns (int112 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt120(uint256 _offst, bytes memory _input) internal pure returns (int120 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt128(uint256 _offst, bytes memory _input) internal pure returns (int128 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt136(uint256 _offst, bytes memory _input) internal pure returns (int136 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt144(uint256 _offst, bytes memory _input) internal pure returns (int144 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt152(uint256 _offst, bytes memory _input) internal pure returns (int152 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt160(uint256 _offst, bytes memory _input) internal pure returns (int160 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt168(uint256 _offst, bytes memory _input) internal pure returns (int168 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt176(uint256 _offst, bytes memory _input) internal pure returns (int176 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt184(uint256 _offst, bytes memory _input) internal pure returns (int184 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt192(uint256 _offst, bytes memory _input) internal pure returns (int192 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt200(uint256 _offst, bytes memory _input) internal pure returns (int200 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt208(uint256 _offst, bytes memory _input) internal pure returns (int208 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt216(uint256 _offst, bytes memory _input) internal pure returns (int216 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt224(uint256 _offst, bytes memory _input) internal pure returns (int224 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt232(uint256 _offst, bytes memory _input) internal pure returns (int232 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt240(uint256 _offst, bytes memory _input) internal pure returns (int240 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt248(uint256 _offst, bytes memory _input) internal pure returns (int248 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToInt256(uint256 _offst, bytes memory _input) internal pure returns (int256 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint8(uint256 _offst, bytes memory _input) internal pure returns (uint8 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint16(uint256 _offst, bytes memory _input) internal pure returns (uint16 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint24(uint256 _offst, bytes memory _input) internal pure returns (uint24 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint32(uint256 _offst, bytes memory _input) internal pure returns (uint32 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint40(uint256 _offst, bytes memory _input) internal pure returns (uint40 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint48(uint256 _offst, bytes memory _input) internal pure returns (uint48 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint56(uint256 _offst, bytes memory _input) internal pure returns (uint56 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint64(uint256 _offst, bytes memory _input) internal pure returns (uint64 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint72(uint256 _offst, bytes memory _input) internal pure returns (uint72 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint80(uint256 _offst, bytes memory _input) internal pure returns (uint80 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint88(uint256 _offst, bytes memory _input) internal pure returns (uint88 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint96(uint256 _offst, bytes memory _input) internal pure returns (uint96 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint104(uint256 _offst, bytes memory _input) internal pure returns (uint104 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint112(uint256 _offst, bytes memory _input) internal pure returns (uint112 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint120(uint256 _offst, bytes memory _input) internal pure returns (uint120 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint128(uint256 _offst, bytes memory _input) internal pure returns (uint128 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint136(uint256 _offst, bytes memory _input) internal pure returns (uint136 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint144(uint256 _offst, bytes memory _input) internal pure returns (uint144 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint152(uint256 _offst, bytes memory _input) internal pure returns (uint152 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint160(uint256 _offst, bytes memory _input) internal pure returns (uint160 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint168(uint256 _offst, bytes memory _input) internal pure returns (uint168 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint176(uint256 _offst, bytes memory _input) internal pure returns (uint176 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint184(uint256 _offst, bytes memory _input) internal pure returns (uint184 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint192(uint256 _offst, bytes memory _input) internal pure returns (uint192 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint200(uint256 _offst, bytes memory _input) internal pure returns (uint200 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint208(uint256 _offst, bytes memory _input) internal pure returns (uint208 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint216(uint256 _offst, bytes memory _input) internal pure returns (uint216 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint224(uint256 _offst, bytes memory _input) internal pure returns (uint224 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint232(uint256 _offst, bytes memory _input) internal pure returns (uint232 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint240(uint256 _offst, bytes memory _input) internal pure returns (uint240 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint248(uint256 _offst, bytes memory _input) internal pure returns (uint248 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
    function bytesToUint256(uint256 _offst, bytes memory _input) internal pure returns (uint256 _output) {
        assembly {
            _output := mload(add(_input, _offst))
        }
    }
}
// contracts/lib/Memory.sol
library Memory {
    // Size of a word, in bytes.
    uint256 internal constant WORD_SIZE = 32;
    // Size of the header of a 'bytes' array.
    uint256 internal constant BYTES_HEADER_SIZE = 32;
    // Address of the free memory pointer.
    uint256 internal constant FREE_MEM_PTR = 0x40;
    // Compares the 'len' bytes starting at address 'addr' in memory with the 'len'
    // bytes starting at 'addr2'.
    // Returns 'true' if the bytes are the same, otherwise 'false'.
    function equals(uint256 addr, uint256 addr2, uint256 len) internal pure returns (bool equal) {
        assembly {
            equal := eq(keccak256(addr, len), keccak256(addr2, len))
        }
    }
    // Compares the 'len' bytes starting at address 'addr' in memory with the bytes stored in
    // 'bts'. It is allowed to set 'len' to a lower value then 'bts.length', in which case only
    // the first 'len' bytes will be compared.
    // Requires that 'bts.length >= len'
    function equals(uint256 addr, uint256 len, bytes memory bts) internal pure returns (bool equal) {
        require(bts.length >= len);
        uint256 addr2;
        assembly {
            addr2 := add(bts, /*BYTES_HEADER_SIZE*/ 32)
        }
        return equals(addr, addr2, len);
    }
    function compareStrings(string memory a, string memory b) internal pure returns (bool) {
        return (keccak256(abi.encodePacked((a))) == keccak256(abi.encodePacked((b))));
    }
    // Copy 'len' bytes from memory address 'src', to address 'dest'.
    // This function does not check the or destination, it only copies
    // the bytes.
    function copy(uint256 src, uint256 dest, uint256 len) internal pure {
        // Copy word-length chunks while possible
        for (; len >= WORD_SIZE; len -= WORD_SIZE) {
            assembly {
                mstore(dest, mload(src))
            }
            dest += WORD_SIZE;
            src += WORD_SIZE;
        }
        // Copy remaining bytes
        uint256 mask = 256 ** (WORD_SIZE - len) - 1;
        assembly {
            let srcpart := and(mload(src), not(mask))
            let destpart := and(mload(dest), mask)
            mstore(dest, or(destpart, srcpart))
        }
    }
    // Returns a memory pointer to the provided bytes array.
    function ptr(bytes memory bts) internal pure returns (uint256 addr) {
        assembly {
            addr := bts
        }
    }
    // Returns a memory pointer to the data portion of the provided bytes array.
    function dataPtr(bytes memory bts) internal pure returns (uint256 addr) {
        assembly {
            addr := add(bts, /*BYTES_HEADER_SIZE*/ 32)
        }
    }
    // This function does the same as 'dataPtr(bytes memory)', but will also return the
    // length of the provided bytes array.
    function fromBytes(bytes memory bts) internal pure returns (uint256 addr, uint256 len) {
        len = bts.length;
        assembly {
            addr := add(bts, /*BYTES_HEADER_SIZE*/ 32)
        }
    }
    // Creates a 'bytes memory' variable from the memory address 'addr', with the
    // length 'len'. The function will allocate new memory for the bytes array, and
    // the 'len bytes starting at 'addr' will be copied into that new memory.
    function toBytes(uint256 addr, uint256 len) internal pure returns (bytes memory bts) {
        bts = new bytes(len);
        uint256 btsptr;
        assembly {
            btsptr := add(bts, /*BYTES_HEADER_SIZE*/ 32)
        }
        copy(addr, btsptr, len);
    }
    // Get the word stored at memory address 'addr' as a 'uint'.
    function toUint(uint256 addr) internal pure returns (uint256 n) {
        assembly {
            n := mload(addr)
        }
    }
    // Get the word stored at memory address 'addr' as a 'bytes32'.
    function toBytes32(uint256 addr) internal pure returns (bytes32 bts) {
        assembly {
            bts := mload(addr)
        }
    }
}
// contracts/MerkleProof.sol
library MerkleProof {
    function validateMerkleProof(
        bytes32 appHash,
        string memory storeName,
        bytes memory key,
        bytes memory value,
        bytes memory proof
    ) internal view returns (bool) {
        if (appHash == bytes32(0)) {
            return false;
        }
        // | storeName | key length | key | value length | value | appHash  | proof |
        // | 32 bytes  | 32 bytes   |   | 32 bytes   |     | 32 bytes |
        bytes memory input = new bytes(128 + key.length + value.length + proof.length);
        uint256 ptr = Memory.dataPtr(input);
        bytes memory storeNameBytes = bytes(storeName);
        /* solium-disable-next-line */
        assembly {
            mstore(ptr, mload(add(storeNameBytes, 32)))
        }
        uint256 src;
        uint256 length;
        // write key length and key to input
        ptr += 32;
        (src, length) = Memory.fromBytes(key);
        /* solium-disable-next-line */
        assembly {
            mstore(ptr, length)
        }
        ptr += 32;
        Memory.copy(src, ptr, length);
        // write value length and value to input
        ptr += length;
        (src, length) = Memory.fromBytes(value);
        /* solium-disable-next-line */
        assembly {
            mstore(ptr, length)
        }
        ptr += 32;
        Memory.copy(src, ptr, length);
        // write appHash to input
        ptr += length;
        /* solium-disable-next-line */
        assembly {
            mstore(ptr, appHash)
        }
        // write proof to input
        ptr += 32;
        (src, length) = Memory.fromBytes(proof);
        Memory.copy(src, ptr, length);
        length = input.length + 32;
        uint256[1] memory result;
        /* solium-disable-next-line */
        assembly {
            // call validateMerkleProof precompile contract
            // Contract address: 0x65
            if iszero(staticcall(not(0), 0x65, input, length, result, 0x20)) { }
        }
        return result[0] == 0x01;
    }
}
// contracts/System.sol
contract System {
    bool public alreadyInit;
    uint32 public constant CODE_OK = 0;
    uint32 public constant ERROR_FAIL_DECODE = 100;
    uint8 public constant BIND_CHANNELID = 0x01;
    uint8 public constant TRANSFER_IN_CHANNELID = 0x02;
    uint8 public constant TRANSFER_OUT_CHANNELID = 0x03;
    uint8 public constant STAKING_CHANNELID = 0x08;
    uint8 public constant GOV_CHANNELID = 0x09;
    uint8 public constant SLASH_CHANNELID = 0x0b;
    uint8 public constant CROSS_STAKE_CHANNELID = 0x10;
    uint8 public constant BC_FUSION_CHANNELID = 0x11; // new channel id for cross-chain redelegate from Beacon Chain to Smart Chain after Feynman upgrade
    uint16 public constant bscChainID = 0x0038;
    address public constant VALIDATOR_CONTRACT_ADDR = 0x0000000000000000000000000000000000001000;
    address public constant SLASH_CONTRACT_ADDR = 0x0000000000000000000000000000000000001001;
    address public constant SYSTEM_REWARD_ADDR = 0x0000000000000000000000000000000000001002;
    address public constant LIGHT_CLIENT_ADDR = 0x0000000000000000000000000000000000001003;
    address public constant TOKEN_HUB_ADDR = 0x0000000000000000000000000000000000001004;
    address public constant INCENTIVIZE_ADDR = 0x0000000000000000000000000000000000001005;
    address public constant RELAYERHUB_CONTRACT_ADDR = 0x0000000000000000000000000000000000001006;
    address public constant GOV_HUB_ADDR = 0x0000000000000000000000000000000000001007;
    address public constant TOKEN_MANAGER_ADDR = 0x0000000000000000000000000000000000001008;
    address public constant CROSS_CHAIN_CONTRACT_ADDR = 0x0000000000000000000000000000000000002000;
    address public constant STAKING_CONTRACT_ADDR = 0x0000000000000000000000000000000000002001;
    address public constant STAKE_HUB_ADDR = 0x0000000000000000000000000000000000002002;
    address public constant STAKE_CREDIT_ADDR = 0x0000000000000000000000000000000000002003;
    address public constant GOVERNOR_ADDR = 0x0000000000000000000000000000000000002004;
    address public constant GOV_TOKEN_ADDR = 0x0000000000000000000000000000000000002005;
    address public constant TIMELOCK_ADDR = 0x0000000000000000000000000000000000002006;
    address public constant TOKEN_RECOVER_PORTAL_ADDR = 0x0000000000000000000000000000000000003000;
    modifier onlyCoinbase() {
        require(msg.sender == block.coinbase, "the message sender must be the block producer");
        _;
    }
    modifier onlyZeroGasPrice() {
        require(tx.gasprice == 0, "gasprice is not zero");
        _;
    }
    modifier onlyNotInit() {
        require(!alreadyInit, "the contract already init");
        _;
    }
    modifier onlyInit() {
        require(alreadyInit, "the contract not init yet");
        _;
    }
    modifier onlySlash() {
        require(msg.sender == SLASH_CONTRACT_ADDR, "the message sender must be slash contract");
        _;
    }
    modifier onlyTokenHub() {
        require(msg.sender == TOKEN_HUB_ADDR, "the message sender must be token hub contract");
        _;
    }
    modifier onlyGov() {
        require(msg.sender == GOV_HUB_ADDR, "the message sender must be governance contract");
        _;
    }
    modifier onlyValidatorContract() {
        require(msg.sender == VALIDATOR_CONTRACT_ADDR, "the message sender must be validatorSet contract");
        _;
    }
    modifier onlyCrossChainContract() {
        require(msg.sender == CROSS_CHAIN_CONTRACT_ADDR, "the message sender must be cross chain contract");
        _;
    }
    modifier onlyRelayerIncentivize() {
        require(msg.sender == INCENTIVIZE_ADDR, "the message sender must be incentivize contract");
        _;
    }
    modifier onlyRelayer() {
        require(IRelayerHub(RELAYERHUB_CONTRACT_ADDR).isRelayer(msg.sender), "the msg sender is not a relayer");
        _;
    }
    modifier onlyTokenManager() {
        require(msg.sender == TOKEN_MANAGER_ADDR, "the msg sender must be tokenManager");
        _;
    }
    modifier onlyStakeHub() {
        require(msg.sender == STAKE_HUB_ADDR, "the msg sender must be stakeHub");
        _;
    }
    modifier onlyGovernorTimelock() {
        require(msg.sender == TIMELOCK_ADDR, "the msg sender must be governor timelock contract");
        _;
    }
    modifier onlyTokenRecoverPortal() {
        require(msg.sender == TOKEN_RECOVER_PORTAL_ADDR, "the msg sender must be token recover portal");
        _;
    }
    // Not reliable, do not use when need strong verify
    function isContract(address addr) internal view returns (bool) {
        uint256 size;
        assembly {
            size := extcodesize(addr)
        }
        return size > 0;
    }
}
// contracts/CrossChain.sol
contract CrossChain is System, ICrossChain, IParamSubscriber {
    // constant variables
    string public constant STORE_NAME = "ibc";
    uint256 public constant CROSS_CHAIN_KEY_PREFIX = 0x01003800; // last 6 bytes
    uint8 public constant SYN_PACKAGE = 0x00;
    uint8 public constant ACK_PACKAGE = 0x01;
    uint8 public constant FAIL_ACK_PACKAGE = 0x02;
    uint256 public constant INIT_BATCH_SIZE = 50;
    // governable parameters
    uint256 public batchSizeForOracle;
    //state variables
    uint256 public previousTxHeight;
    uint256 public txCounter;
    int64 public oracleSequence;
    mapping(uint8 => address) public channelHandlerContractMap;
    mapping(address => mapping(uint8 => bool)) public registeredContractChannelMap;
    mapping(uint8 => uint64) public channelSendSequenceMap;
    mapping(uint8 => uint64) public channelReceiveSequenceMap;
    mapping(uint8 => bool) public isRelayRewardFromSystemReward;
    // to prevent the utilization of ancient block header
    mapping(uint8 => uint64) public channelSyncedHeaderMap;
    // BEP-171: Security Enhancement for Cross-Chain Module
    // 0xebbda044f67428d7e9b472f9124983082bcda4f84f5148ca0a9ccbe06350f196
    bytes32 public constant SUSPEND_PROPOSAL = keccak256("SUSPEND_PROPOSAL");
    // 0xcf82004e82990eca84a75e16ba08aa620238e076e0bc7fc4c641df44bbf5b55a
    bytes32 public constant REOPEN_PROPOSAL = keccak256("REOPEN_PROPOSAL");
    // 0x605b57daa79220f76a5cdc8f5ee40e59093f21a4e1cec30b9b99c555e94c75b9
    bytes32 public constant CANCEL_TRANSFER_PROPOSAL = keccak256("CANCEL_TRANSFER_PROPOSAL");
    // 0xc5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470
    bytes32 public constant EMPTY_CONTENT_HASH = keccak256("");
    uint16 public constant INIT_SUSPEND_QUORUM = 1;
    uint16 public constant INIT_REOPEN_QUORUM = 2;
    uint16 public constant INIT_CANCEL_TRANSFER_QUORUM = 2;
    uint256 public constant EMERGENCY_PROPOSAL_EXPIRE_PERIOD = 1 hours;
    bool public isSuspended;
    // proposal type hash => latest emergency proposal
    mapping(bytes32 => EmergencyProposal) public emergencyProposals;
    // proposal type hash => the threshold of proposal approved
    mapping(bytes32 => uint16) public quorumMap;
    // IAVL key hash => is challenged
    mapping(bytes32 => bool) public challenged;
    // struct
    // BEP-171: Security Enhancement for Cross-Chain Module
    struct EmergencyProposal {
        uint16 quorum;
        uint128 expiredAt;
        bytes32 contentHash;
        address[] approvers;
    }
    // event
    event crossChainPackage(
        uint16 chainId,
        uint64 indexed oracleSequence,
        uint64 indexed packageSequence,
        uint8 indexed channelId,
        bytes payload
    );
    event receivedPackage(uint8 packageType, uint64 indexed packageSequence, uint8 indexed channelId);
    event unsupportedPackage(uint64 indexed packageSequence, uint8 indexed channelId, bytes payload);
    event unexpectedRevertInPackageHandler(address indexed contractAddr, string reason);
    event unexpectedFailureAssertionInPackageHandler(address indexed contractAddr, bytes lowLevelData);
    event paramChange(string key, bytes value);
    event enableOrDisableChannel(uint8 indexed channelId, bool isEnable);
    event addChannel(uint8 indexed channelId, address indexed contractAddr);
    // BEP-171: Security Enhancement for Cross-Chain Module
    event ProposalSubmitted(
        bytes32 indexed proposalTypeHash,
        address indexed proposer,
        uint128 quorum,
        uint128 expiredAt,
        bytes32 contentHash
    );
    event Suspended(address indexed executor);
    event Reopened(address indexed executor);
    event SuccessChallenge(address indexed challenger, uint64 packageSequence, uint8 channelId);
    modifier sequenceInOrder(uint64 _sequence, uint8 _channelID) {
        uint64 expectedSequence = channelReceiveSequenceMap[_channelID];
        require(_sequence == expectedSequence, "sequence not in order");
        channelReceiveSequenceMap[_channelID] = expectedSequence + 1;
        _;
    }
    modifier blockSynced(uint64 _height) {
        require(ILightClient(LIGHT_CLIENT_ADDR).isHeaderSynced(_height), "light client not sync the block yet");
        _;
    }
    modifier channelSupported(uint8 _channelID) {
        require(channelHandlerContractMap[_channelID] != address(0x0), "channel is not supported");
        _;
    }
    modifier onlyRegisteredContractChannel(uint8 channleId) {
        require(
            registeredContractChannelMap[msg.sender][channleId], "the contract and channel have not been registered"
        );
        _;
    }
    modifier headerInOrder(uint64 height, uint8 channelId) {
        require(height >= channelSyncedHeaderMap[channelId], "too old header");
        if (height != channelSyncedHeaderMap[channelId]) {
            channelSyncedHeaderMap[channelId] = height;
        }
        _;
    }
    // BEP-171: Security Enhancement for Cross-Chain Module
    modifier onlyCabinet() {
        uint256 indexPlus = IBSCValidatorSetV2(VALIDATOR_CONTRACT_ADDR).currentValidatorSetMap(msg.sender);
        uint256 numOfCabinets = IBSCValidatorSetV2(VALIDATOR_CONTRACT_ADDR).numOfCabinets();
        if (numOfCabinets == 0) {
            numOfCabinets = 21;
        }
        require(indexPlus > 0 && indexPlus <= numOfCabinets, "not cabinet");
        _;
    }
    modifier whenNotSuspended() {
        require(!isSuspended, "suspended");
        _;
    }
    modifier whenSuspended() {
        require(isSuspended, "not suspended");
        _;
    }
    // | length   | prefix | sourceChainID| destinationChainID | channelID | sequence |
    // | 32 bytes | 1 byte | 2 bytes      | 2 bytes            |  1 bytes  | 8 bytes  |
    function generateKey(uint64 _sequence, uint8 _channelID) internal pure returns (bytes memory) {
        uint256 fullCROSS_CHAIN_KEY_PREFIX = CROSS_CHAIN_KEY_PREFIX | _channelID;
        bytes memory key = new bytes(14);
        uint256 ptr;
        assembly {
            ptr := add(key, 14)
        }
        assembly {
            mstore(ptr, _sequence)
        }
        ptr -= 8;
        assembly {
            mstore(ptr, fullCROSS_CHAIN_KEY_PREFIX)
        }
        ptr -= 6;
        assembly {
            mstore(ptr, 14)
        }
        return key;
    }
    function init() external onlyNotInit {
        channelHandlerContractMap[BIND_CHANNELID] = TOKEN_MANAGER_ADDR;
        isRelayRewardFromSystemReward[BIND_CHANNELID] = false;
        registeredContractChannelMap[TOKEN_MANAGER_ADDR][BIND_CHANNELID] = true;
        channelHandlerContractMap[TRANSFER_IN_CHANNELID] = TOKEN_HUB_ADDR;
        isRelayRewardFromSystemReward[TRANSFER_IN_CHANNELID] = false;
        registeredContractChannelMap[TOKEN_HUB_ADDR][TRANSFER_IN_CHANNELID] = true;
        channelHandlerContractMap[TRANSFER_OUT_CHANNELID] = TOKEN_HUB_ADDR;
        isRelayRewardFromSystemReward[TRANSFER_OUT_CHANNELID] = false;
        registeredContractChannelMap[TOKEN_HUB_ADDR][TRANSFER_OUT_CHANNELID] = true;
        channelHandlerContractMap[STAKING_CHANNELID] = VALIDATOR_CONTRACT_ADDR;
        isRelayRewardFromSystemReward[STAKING_CHANNELID] = true;
        registeredContractChannelMap[VALIDATOR_CONTRACT_ADDR][STAKING_CHANNELID] = true;
        channelHandlerContractMap[GOV_CHANNELID] = GOV_HUB_ADDR;
        isRelayRewardFromSystemReward[GOV_CHANNELID] = true;
        registeredContractChannelMap[GOV_HUB_ADDR][GOV_CHANNELID] = true;
        channelHandlerContractMap[SLASH_CHANNELID] = SLASH_CONTRACT_ADDR;
        isRelayRewardFromSystemReward[SLASH_CHANNELID] = true;
        registeredContractChannelMap[SLASH_CONTRACT_ADDR][SLASH_CHANNELID] = true;
        batchSizeForOracle = INIT_BATCH_SIZE;
        oracleSequence = -1;
        previousTxHeight = 0;
        txCounter = 0;
        alreadyInit = true;
    }
    function encodePayload(
        uint8 packageType,
        uint256 relayFee,
        bytes memory msgBytes
    ) public pure returns (bytes memory) {
        uint256 payloadLength = msgBytes.length + 33;
        bytes memory payload = new bytes(payloadLength);
        uint256 ptr;
        assembly {
            ptr := payload
        }
        ptr += 33;
        assembly {
            mstore(ptr, relayFee)
        }
        ptr -= 32;
        assembly {
            mstore(ptr, packageType)
        }
        ptr -= 1;
        assembly {
            mstore(ptr, payloadLength)
        }
        ptr += 65;
        (uint256 src,) = Memory.fromBytes(msgBytes);
        Memory.copy(src, ptr, msgBytes.length);
        return payload;
    }
    // | type   | relayFee   |package  |
    // | 1 byte | 32 bytes   | bytes    |
    function decodePayloadHeader(bytes memory payload) internal pure returns (bool, uint8, uint256, bytes memory) {
        if (payload.length < 33) {
            return (false, 0, 0, new bytes(0));
        }
        uint256 ptr;
        assembly {
            ptr := payload
        }
        uint8 packageType;
        ptr += 1;
        assembly {
            packageType := mload(ptr)
        }
        uint256 relayFee;
        ptr += 32;
        assembly {
            relayFee := mload(ptr)
        }
        ptr += 32;
        bytes memory msgBytes = new bytes(payload.length - 33);
        (uint256 dst,) = Memory.fromBytes(msgBytes);
        Memory.copy(ptr, dst, payload.length - 33);
        return (true, packageType, relayFee, msgBytes);
    }
    function handlePackage(
        bytes calldata payload,
        bytes calldata proof,
        uint64 height,
        uint64 packageSequence,
        uint8 channelId
    )
        external
        onlyInit
        onlyRelayer
        sequenceInOrder(packageSequence, channelId)
        blockSynced(height)
        channelSupported(channelId)
        headerInOrder(height, channelId)
        whenNotSuspended
    {
        bytes memory payloadLocal = payload; // fix error: stack too deep, try removing local variables
        bytes memory proofLocal = proof; // fix error: stack too deep, try removing local variables
        require(
            MerkleProof.validateMerkleProof(
                ILightClient(LIGHT_CLIENT_ADDR).getAppHash(height),
                STORE_NAME,
                generateKey(packageSequence, channelId),
                payloadLocal,
                proofLocal
            ),
            "invalid merkle proof"
        );
        address payable headerRelayer = ILightClient(LIGHT_CLIENT_ADDR).getSubmitter(height);
        uint64 sequenceLocal = packageSequence; // fix error: stack too deep, try removing local variables
        uint8 channelIdLocal = channelId; // fix error: stack too deep, try removing local variables
        (bool success, uint8 packageType, uint256 relayFee, bytes memory msgBytes) = decodePayloadHeader(payloadLocal);
        if (!success) {
            emit unsupportedPackage(sequenceLocal, channelIdLocal, payloadLocal);
            return;
        }
        emit receivedPackage(packageType, sequenceLocal, channelIdLocal);
        if (packageType == SYN_PACKAGE) {
            address handlerContract = channelHandlerContractMap[channelIdLocal];
            try IApplication(handlerContract).handleSynPackage(channelIdLocal, msgBytes) returns (
                bytes memory responsePayload
            ) {
                if (responsePayload.length != 0) {
                    sendPackage(
                        channelSendSequenceMap[channelIdLocal],
                        channelIdLocal,
                        encodePayload(ACK_PACKAGE, 0, responsePayload)
                    );
                    channelSendSequenceMap[channelIdLocal] = channelSendSequenceMap[channelIdLocal] + 1;
                }
            } catch Error(string memory reason) {
                sendPackage(
                    channelSendSequenceMap[channelIdLocal], channelIdLocal, encodePayload(FAIL_ACK_PACKAGE, 0, msgBytes)
                );
                channelSendSequenceMap[channelIdLocal] = channelSendSequenceMap[channelIdLocal] + 1;
                emit unexpectedRevertInPackageHandler(handlerContract, reason);
            } catch (bytes memory lowLevelData) {
                sendPackage(
                    channelSendSequenceMap[channelIdLocal], channelIdLocal, encodePayload(FAIL_ACK_PACKAGE, 0, msgBytes)
                );
                channelSendSequenceMap[channelIdLocal] = channelSendSequenceMap[channelIdLocal] + 1;
                emit unexpectedFailureAssertionInPackageHandler(handlerContract, lowLevelData);
            }
        } else if (packageType == ACK_PACKAGE) {
            address handlerContract = channelHandlerContractMap[channelIdLocal];
            try IApplication(handlerContract).handleAckPackage(channelIdLocal, msgBytes) { }
            catch Error(string memory reason) {
                emit unexpectedRevertInPackageHandler(handlerContract, reason);
            } catch (bytes memory lowLevelData) {
                emit unexpectedFailureAssertionInPackageHandler(handlerContract, lowLevelData);
            }
        } else if (packageType == FAIL_ACK_PACKAGE) {
            address handlerContract = channelHandlerContractMap[channelIdLocal];
            try IApplication(handlerContract).handleFailAckPackage(channelIdLocal, msgBytes) { }
            catch Error(string memory reason) {
                emit unexpectedRevertInPackageHandler(handlerContract, reason);
            } catch (bytes memory lowLevelData) {
                emit unexpectedFailureAssertionInPackageHandler(handlerContract, lowLevelData);
            }
        }
        IRelayerIncentivize(INCENTIVIZE_ADDR).addReward(
            headerRelayer,
            msg.sender,
            relayFee,
            isRelayRewardFromSystemReward[channelIdLocal] || packageType != SYN_PACKAGE
        );
    }
    function sendPackage(uint64 packageSequence, uint8 channelId, bytes memory payload) internal whenNotSuspended {
        if (block.number > previousTxHeight) {
            ++oracleSequence;
            txCounter = 1;
            previousTxHeight = block.number;
        } else {
            ++txCounter;
            if (txCounter > batchSizeForOracle) {
                ++oracleSequence;
                txCounter = 1;
            }
        }
        emit crossChainPackage(bscChainID, uint64(oracleSequence), packageSequence, channelId, payload);
    }
    function sendSynPackage(
        uint8 channelId,
        bytes calldata msgBytes,
        uint256 relayFee
    ) external override onlyInit onlyRegisteredContractChannel(channelId) {
        uint64 sendSequence = channelSendSequenceMap[channelId];
        sendPackage(sendSequence, channelId, encodePayload(SYN_PACKAGE, relayFee, msgBytes));
        ++sendSequence;
        channelSendSequenceMap[channelId] = sendSequence;
    }
    function updateParam(string calldata key, bytes calldata value) external override onlyGov whenNotSuspended {
        if (Memory.compareStrings(key, "batchSizeForOracle")) {
            uint256 newBatchSizeForOracle = BytesToTypes.bytesToUint256(32, value);
            require(
                newBatchSizeForOracle <= 10000 && newBatchSizeForOracle >= 10,
                "the newBatchSizeForOracle should be in [10, 10000]"
            );
            batchSizeForOracle = newBatchSizeForOracle;
        } else if (Memory.compareStrings(key, "addOrUpdateChannel")) {
            bytes memory valueLocal = value;
            require(
                valueLocal.length == 22,
                "length of value for addOrUpdateChannel should be 22, channelId:isFromSystem:handlerAddress"
            );
            uint8 channelId;
            assembly {
                channelId := mload(add(valueLocal, 1))
            }
            uint8 rewardConfig;
            assembly {
                rewardConfig := mload(add(valueLocal, 2))
            }
            bool isRewardFromSystem = (rewardConfig == 0x0);
            address handlerContract;
            assembly {
                handlerContract := mload(add(valueLocal, 22))
            }
            require(isContract(handlerContract), "address is not a contract");
            channelHandlerContractMap[channelId] = handlerContract;
            registeredContractChannelMap[handlerContract][channelId] = true;
            isRelayRewardFromSystemReward[channelId] = isRewardFromSystem;
            emit addChannel(channelId, handlerContract);
        } else if (Memory.compareStrings(key, "enableOrDisableChannel")) {
            bytes memory valueLocal = value;
            require(
                valueLocal.length == 2, "length of value for enableOrDisableChannel should be 2, channelId:isEnable"
            );
            uint8 channelId;
            assembly {
                channelId := mload(add(valueLocal, 1))
            }
            uint8 status;
            assembly {
                status := mload(add(valueLocal, 2))
            }
            bool isEnable = (status == 1);
            address handlerContract = channelHandlerContractMap[channelId];
            if (handlerContract != address(0x00)) {
                //channel existing
                registeredContractChannelMap[handlerContract][channelId] = isEnable;
                emit enableOrDisableChannel(channelId, isEnable);
            }
        } else if (Memory.compareStrings(key, "suspendQuorum")) {
            require(value.length == 2, "length of value for suspendQuorum should be 2");
            uint16 suspendQuorum = BytesToTypes.bytesToUint16(2, value);
            require(suspendQuorum > 0 && suspendQuorum < 100, "invalid suspend quorum");
            quorumMap[SUSPEND_PROPOSAL] = suspendQuorum;
        } else if (Memory.compareStrings(key, "reopenQuorum")) {
            require(value.length == 2, "length of value for reopenQuorum should be 2");
            uint16 reopenQuorum = BytesToTypes.bytesToUint16(2, value);
            require(reopenQuorum > 0 && reopenQuorum < 100, "invalid reopen quorum");
            quorumMap[REOPEN_PROPOSAL] = reopenQuorum;
        } else if (Memory.compareStrings(key, "cancelTransferQuorum")) {
            require(value.length == 2, "length of value for cancelTransferQuorum should be 2");
            uint16 cancelTransferQuorum = BytesToTypes.bytesToUint16(2, value);
            require(cancelTransferQuorum > 0 && cancelTransferQuorum < 100, "invalid cancel transfer quorum");
            quorumMap[CANCEL_TRANSFER_PROPOSAL] = cancelTransferQuorum;
        } else {
            require(false, "unknown param");
        }
        emit paramChange(key, value);
    }
    // BEP-171: Security Enhancement for Cross-Chain Module
    function challenge(
        // to avoid stack too deep error, using `uint64[4] calldata params`
        // instead of  `uint64 height0, uint64 height1, uint64 packageSequence, uint8 channelId`
        uint64[4] calldata params, // 0-height0, 1-height1, 2-packageSequence, 3-channelId,
        bytes calldata payload0,
        bytes calldata payload1,
        bytes calldata proof0,
        bytes calldata proof1
    )
        external
        onlyInit
        blockSynced(params[0])
        blockSynced(params[1])
        channelSupported(uint8(params[3]))
        whenNotSuspended
    {
        // the same key with different values (payloads)
        require(keccak256(payload0) != keccak256(payload1), "same payload");
        bytes memory _key;
        uint64 _packageSequence;
        uint8 _channelId;
        {
            _packageSequence = params[2];
            _channelId = uint8(params[3]);
            _key = generateKey(_packageSequence, _channelId);
            bytes32 _keyHash = keccak256(_key);
            require(!challenged[_keyHash], "already challenged");
            // if succeeding in challenge
            challenged[_keyHash] = true;
        }
        // verify payload0 + proof0
        {
            uint64 _height0 = params[0];
            bytes memory _payload0 = payload0;
            bytes memory _proof0 = proof0;
            bytes32 _appHash0 = ILightClient(LIGHT_CLIENT_ADDR).getAppHash(_height0);
            require(
                MerkleProof.validateMerkleProof(_appHash0, STORE_NAME, _key, _payload0, _proof0),
                "invalid merkle proof0"
            );
        }
        // verify payload1 + proof1
        {
            uint64 _height1 = params[1];
            bytes memory _payload1 = payload1;
            bytes memory _proof1 = proof1;
            bytes32 _appHash1 = ILightClient(LIGHT_CLIENT_ADDR).getAppHash(_height1);
            require(
                MerkleProof.validateMerkleProof(_appHash1, STORE_NAME, _key, _payload1, _proof1),
                "invalid merkle proof1"
            );
        }
        _suspend();
        emit SuccessChallenge(msg.sender, _packageSequence, _channelId);
    }
    function suspend() external onlyInit onlyCabinet whenNotSuspended {
        bool isExecutable = _approveProposal(SUSPEND_PROPOSAL, EMPTY_CONTENT_HASH);
        if (isExecutable) {
            _suspend();
        }
    }
    function reopen() external onlyInit onlyCabinet whenSuspended {
        bool isExecutable = _approveProposal(REOPEN_PROPOSAL, EMPTY_CONTENT_HASH);
        if (isExecutable) {
            isSuspended = false;
            emit Reopened(msg.sender);
        }
    }
    function cancelTransfer(address tokenAddr, address attacker) external onlyInit onlyCabinet {
        bytes32 _contentHash = keccak256(abi.encode(tokenAddr, attacker));
        bool isExecutable = _approveProposal(CANCEL_TRANSFER_PROPOSAL, _contentHash);
        if (isExecutable) {
            ITokenHub(TOKEN_HUB_ADDR).cancelTransferIn(tokenAddr, attacker);
        }
    }
    function _approveProposal(bytes32 proposalTypeHash, bytes32 _contentHash) internal returns (bool isExecutable) {
        if (quorumMap[proposalTypeHash] == 0) {
            quorumMap[SUSPEND_PROPOSAL] = INIT_SUSPEND_QUORUM;
            quorumMap[REOPEN_PROPOSAL] = INIT_REOPEN_QUORUM;
            quorumMap[CANCEL_TRANSFER_PROPOSAL] = INIT_CANCEL_TRANSFER_QUORUM;
        }
        EmergencyProposal storage p = emergencyProposals[proposalTypeHash];
        // It is ok if there is an evil validator always cancel the previous vote,
        // the credible validator could use private transaction service to send a batch tx including 2 approve transactions
        if (block.timestamp >= p.expiredAt || p.contentHash != _contentHash) {
            // current proposal expired / not exist or not same with the new, create a new EmergencyProposal
            p.quorum = quorumMap[proposalTypeHash];
            p.expiredAt = uint128(block.timestamp + EMERGENCY_PROPOSAL_EXPIRE_PERIOD);
            p.contentHash = _contentHash;
            p.approvers = [msg.sender];
            emit ProposalSubmitted(proposalTypeHash, msg.sender, p.quorum, p.expiredAt, _contentHash);
        } else {
            // current proposal exists
            for (uint256 i = 0; i < p.approvers.length; ++i) {
                require(p.approvers[i] != msg.sender, "already approved");
            }
            p.approvers.push(msg.sender);
        }
        if (p.approvers.length >= p.quorum) {
            // 1. remove current proposal
            delete emergencyProposals[proposalTypeHash];
            // 2. exec this proposal
            return true;
        }
        return false;
    }
    function _suspend() internal whenNotSuspended {
        isSuspended = true;
        emit Suspended(msg.sender);
    }
}