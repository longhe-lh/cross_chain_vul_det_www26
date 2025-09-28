# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: L1UserTxEvent1, WithdrawEvent2
- **rel_chain**: ForgeBatch
- **det_chain**: WithdrawEvent1, L1UserTxEvent2
### src_chain: Layer1
- **事件**: L1UserTxEvent1
  - 函数: addL1Transaction
  - 关键操作: require(tokenID < tokenList.length, "Hermez::addL1Transaction: TOKEN_NOT_REGISTERED"), uint256 loadAmount = _float2Fix(loadAmountF), require(loadAmount < _LIMIT_LOAD_AMOUNT, "Hermez::addL1Transaction: LOADAMOUNT_EXCEED_LIMIT"), require(loadAmount == msg.value, "Hermez::addL1Transaction: LOADAMOUNT_ETH_DOES_NOT_MATCH"), require(msg.value == 0, "Hermez::addL1Transaction: MSG_VALUE_NOT_EQUAL_0"), _safeTransferFrom(tokenList[tokenID], msg.sender, address(this), loadAmount), uint256 postBalance = IERC20(tokenList[tokenID]).balanceOf(address(this)), require(postBalance - prevBalance == loadAmount, "Hermez::addL1Transaction: LOADAMOUNT_ERC20_DOES_NOT_MATCH")
- **事件**: WithdrawEvent2
  - 函数: withdrawMerkleProof
  - 关键操作: require(exitNullifierMap[numExitRoot][idx] == false, "Hermez::withdrawMerkleProof: WITHDRAW_ALREADY_DONE"), require(_smtVerifier(exitRoot, siblings, idx, stateHash) == true, "Hermez::withdrawMerkleProof: SMT_PROOF_INVALID"), exitNullifierMap[numExitRoot][idx] = true, _withdrawFunds(amount, tokenID, instantWithdraw)
### rel_chain: RelayChain
- **事件**: ForgeBatch
  - 函数: forgeBatch
  - 关键操作: require(msg.sender == tx.origin, "Hermez::forgeBatch: INTENAL_TX_NOT_ALLOWED"), require(hermezAuctionContract.canForge(msg.sender, block.number) == true, "Hermez::forgeBatch: AUCTION_DENIED"), require(block.number < (lastL1L2Batch + forgeL1L2BatchTimeout), "Hermez::forgeBatch: L1L2BATCH_REQUIRED"), require(rollupVerifiers[verifierIdx].verifierInterface.verifyProof(proofA, proofB, proofC, [input]), "Hermez::forgeBatch: INVALID_PROOF"), lastForgedBatch++, lastIdx = newLastIdx, stateRootMap[lastForgedBatch] = newStRoot, exitRootsMap[lastForgedBatch] = newExitRoot, l1L2TxsDataHashMap[lastForgedBatch] = sha256(l1L2TxsData), lastL1L2Batch = uint64(block.number), l1UserTxsLen = _clearQueue(), hermezAuctionContract.forge(msg.sender)
### det_chain: Layer2
- **事件**: WithdrawEvent1
  - 函数: withdrawCircuit
  - 关键操作: require(exitNullifierMap[numExitRoot][idx] == false, "Hermez::withdrawCircuit: WITHDRAW_ALREADY_DONE"), require(withdrawVerifier.verifyProof(proofA, proofB, proofC, [input]) == true, "Hermez::withdrawCircuit: INVALID_ZK_PROOF"), exitNullifierMap[numExitRoot][idx] = true, _withdrawFunds(amount, tokenID, instantWithdraw)
- **事件**: L1UserTxEvent2
  - 函数: addL1Transaction
  - 关键操作: require(tokenID < tokenList.length, "Hermez::addL1Transaction: TOKEN_NOT_REGISTERED"), uint256 loadAmount = _float2Fix(loadAmountF), require(loadAmount < _LIMIT_LOAD_AMOUNT, "Hermez::addL1Transaction: LOADAMOUNT_EXCEED_LIMIT"), require(loadAmount == msg.value, "Hermez::addL1Transaction: LOADAMOUNT_ETH_DOES_NOT_MATCH"), require(msg.value == 0, "Hermez::addL1Transaction: MSG_VALUE_NOT_EQUAL_0"), _safeTransferFrom(tokenList[tokenID], msg.sender, address(this), loadAmount), uint256 postBalance = IERC20(tokenList[tokenID]).balanceOf(address(this)), require(postBalance - prevBalance == loadAmount, "Hermez::addL1Transaction: LOADAMOUNT_ERC20_DOES_NOT_MATCH")
---
