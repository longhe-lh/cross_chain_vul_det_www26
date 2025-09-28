# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: BlockSubmission
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: SourceChain
- **事件**: TokenDeposit1
  - 函数: deposit
  - 关键操作: require(msg.value >= depositFeeETH, "INSUFFICIENT_DEPOSIT_FEE"), S.pendingDeposits[to][tokenID] = _deposit, emit DepositRequested(from, to, tokenAddress, tokenID, amountDeposited)
- **事件**: TokenRedeem2
  - 函数: forceWithdraw
  - 关键操作: require(S.getNumAvailableForcedSlots() > 0, "TOO_MANY_REQUESTS_OPEN"), S.pendingForcedWithdrawals[accountID][tokenID] = ForcedWithdrawal({owner: owner, timestamp: uint64(block.timestamp)})
### rel_chain: RelayChain
- **事件**: BlockSubmission
  - 函数: submitBlocks
  - 关键操作: require(!S.isInWithdrawalMode(), "INVALID_MODE"), blockVerifier.verifyProofs(...)
### det_chain: DestinationChain
- **事件**: TokenWithdraw1
  - 函数: withdrawFromMerkleTree
  - 关键操作: require(S.isInWithdrawalMode(), "NOT_IN_WITHDRAW_MODE"), ExchangeBalances.verifyAccountBalance(uint(S.merkleAssetRoot()), merkleProof)
- **事件**: TokenMint2
  - 函数: withdrawFromDepositRequest
  - 关键操作: require(deposit.timestamp != 0, "DEPOSIT_NOT_WITHDRAWABLE_YET"), delete S.pendingDeposits[from][tokenID]
---
