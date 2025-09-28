# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: register, deregister
- **rel_chain**: slashDuplicatePropose, slashDuplicatePrevote, slashDuplicatePrecommit, slashSecretReveal
- **det_chain**: claim
### src_chain: SourceChain
- **事件**: register
  - 函数: register
  - 关键操作: require(ren.transferFrom(msg.sender, address(store), minimumBond), "DarknodeRegistry: bond transfer failed")
- **事件**: deregister
  - 函数: deregister
  - 关键操作: deregisterDarknode(_darknodeID)
### rel_chain: RelayChain
- **事件**: slashDuplicatePropose
  - 函数: slashDuplicatePropose
  - 关键操作: address signer = Validate.duplicatePropose(...), slashed[_height][_round][signer] = true, darknodeRegistry.slash(signer, msg.sender, maliciousSlashPercent)
- **事件**: slashDuplicatePrevote
  - 函数: slashDuplicatePrevote
  - 关键操作: address signer = Validate.duplicatePrevote(...), slashed[_height][_round][signer] = true, darknodeRegistry.slash(signer, msg.sender, maliciousSlashPercent)
- **事件**: slashDuplicatePrecommit
  - 函数: slashDuplicatePrecommit
  - 关键操作: address signer = Validate.duplicatePrecommit(...), slashed[_height][_round][signer] = true, darknodeRegistry.slash(signer, msg.sender, maliciousSlashPercent)
- **事件**: slashSecretReveal
  - 函数: slashSecretReveal
  - 关键操作: address signer = Validate.recoverSecret(...), secretRevealed[signer] = true, darknodeRegistry.slash(signer, msg.sender, secretRevealSlashPercent)
### det_chain: DestinationChain
- **事件**: claim
  - 函数: claim
  - 关键操作: _claimDarknodeReward(_darknode)
---
