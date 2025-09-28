# 跨链桥合约分析报告
## 跨链桥: EYWA Bridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenDeposit1, TokenRedeem2
- **rel_chain**: RelayMessage
- **det_chain**: TokenWithdraw1, TokenMint2
### src_chain: SourceChain
- **事件**: TokenDeposit1
  - 函数: sendV2
  - 关键操作: require(state == State.Active, "Bridge: state inactive"), require(previousEpoch.isSet() || currentEpoch.isSet(), "Bridge: epoch not set"), verifyAndUpdateNonce(from, nonce)
- **事件**: TokenRedeem2
  - 函数: receiveV2
  - 关键操作: require(state != State.Inactive, "Bridge: state inactive")
### rel_chain: RelayChain
- **事件**: RelayMessage
  - 函数: verifyMultisig
  - 关键操作: require(popcnt(votersMask) > (uint256(epoch.participantsCount) * 2) / 3, "Block: not enough participants"), require(epoch.participantsCount == 255 || votersMask < (1 << epoch.participantsCount), "Block: bitmask too big"), require(Bls.verifyMultisig(epoch, votersPubKey, blockHeader, votersSignature, votersMask), "Block: multisig mismatch")
### det_chain: DestinationChain
- **事件**: TokenWithdraw1
  - 函数: receiveValidatedData
- **事件**: TokenMint2
  - 函数: functionCall
  - 关键操作: require(abi.decode(result, (bool)), "Bridge: check failed")
---
