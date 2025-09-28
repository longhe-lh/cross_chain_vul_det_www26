# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: LockEvent1
- **rel_chain**: CrossChainEvent, VerifyHeaderAndExecuteTxEvent
- **det_chain**: UnlockEvent1
### src_chain: Ethereum
- **事件**: LockEvent1
  - 函数: lock
  - 关键操作: require(amount != 0, "amount cannot be zero!"), require(_transferToContract(fromAssetHash, amount), "transfer asset from fromAddress to lock_proxy contract  failed!"), require(toAssetHash.length != 0, "empty illegal toAssetHash"), require(toProxyHash.length != 0, "empty illegal toProxyHash"), require(eccm.crossChain(toChainId, toProxyHash, "unlock", txData), "EthCrossChainManager crossChain executed error!")
### rel_chain: PolyChain
- **事件**: CrossChainEvent
  - 函数: crossChain
  - 关键操作: require(whiteListFromContract[msg.sender],"Invalid from contract"), require(eccd.putEthTxHash(keccak256(rawParam)), "Save ethTxHash by index to Data contract failed!")
- **事件**: VerifyHeaderAndExecuteTxEvent
  - 函数: verifyHeaderAndExecuteTx
  - 关键操作: require(ECCUtils.verifySig(rawHeader, headerSig, polyChainBKs, n - ( n - 1) / 3), "Verify poly chain header signature failed!"), require(ECCUtils.verifySig(curRawHeader, headerSig, polyChainBKs, n - ( n - 1) / 3), "Verify poly chain current epoch header signature failed!"), require(ECCUtils.merkleProve(headerProof, curHeader.blockRoot), "verify header proof failed!"), require(!eccd.checkIfFromChainTxExist(toMerkleValue.fromChainID, Utils.bytesToBytes32(toMerkleValue.txHash)), "the transaction has been executed!"), require(eccd.markFromChainTxExist(toMerkleValue.fromChainID, Utils.bytesToBytes32(toMerkleValue.txHash)), "Save crosschain tx exist failed!"), require(toMerkleValue.makeTxParam.toChainId == chainId, "This Tx is not aiming at this network!"), require(whiteListContractMethodMap[toContract][toMerkleValue.makeTxParam.method],"Invalid to contract or method"), require(_executeCrossChainTx(toContract, toMerkleValue.makeTxParam.method, toMerkleValue.makeTxParam.args, toMerkleValue.makeTxParam.fromContract, toMerkleValue.fromChainID), "Execute CrossChain Tx failed!")
### det_chain: DestinationChain
- **事件**: UnlockEvent1
  - 函数: unlock
  - 关键操作: require(fromContractAddr.length != 0, "from proxy contract address cannot be empty"), require(Utils.equalStorage(proxyHashMap[fromChainId], fromContractAddr), "From Proxy contract address error!"), require(args.toAssetHash.length != 0, "toAssetHash cannot be empty"), require(args.toAddress.length != 0, "toAddress cannot be empty"), require(_transferFromContract(toAssetHash, toAddress, args.amount), "transfer asset from lock_proxy contract to toAddress failed!")
---
