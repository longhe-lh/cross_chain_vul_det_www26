# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SwapEthToTon1, SwapTonToEth2
- **rel_chain**: voteForMinting, voteForNewOracleSet, voteForSwitchBurn
- **det_chain**: SwapTonToEth1, SwapEthToTon2
### src_chain: TON
- **事件**: SwapEthToTon1
  - 函数: burn
  - 关键操作: require(allowBurn, "Burn is currently disabled");, _burn(msg.sender, amount);
- **事件**: SwapTonToEth2
  - 函数: mint
  - 关键操作: _mint(sd.receiver, sd.amount);
### rel_chain: RelayChain
- **事件**: voteForMinting
  - 函数: voteForMinting
  - 关键操作: bytes32 _id = getSwapDataId(data);, generalVote(_id, signatures);, executeMinting(data);
- **事件**: voteForNewOracleSet
  - 函数: voteForNewOracleSet
  - 关键操作: bytes32 _id = getNewSetId(oracleSetHash, newOracles);, require(newOracles.length > 2, "New set is too short");, generalVote(_id, signatures);, updateOracleSet(oracleSetHash, newOracles);
- **事件**: voteForSwitchBurn
  - 函数: voteForSwitchBurn
  - 关键操作: bytes32 _id = getNewBurnStatusId(newBurnStatus, nonce);, generalVote(_id, signatures);, allowBurn = newBurnStatus;
### det_chain: EVM
- **事件**: SwapTonToEth1
  - 函数: mint
  - 关键操作: _mint(sd.receiver, sd.amount);
- **事件**: SwapEthToTon2
  - 函数: burn
  - 关键操作: require(allowBurn, "Burn is currently disabled");, _burn(msg.sender, amount);
---
