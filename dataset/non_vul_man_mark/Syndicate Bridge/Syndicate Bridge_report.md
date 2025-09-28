# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Enter1
- **rel_chain**: CosignerAdded, CosignerRemoved
- **det_chain**: Exit1
### src_chain: source_chain
- **事件**: Enter1
  - 函数: enter
  - 关键操作: require(token != address(0), "BR: ZERO_ADDRESS"), require(amount != 0, "BR: ZERO_AMOUNT")
### rel_chain: relay_chain
- **事件**: CosignerAdded
  - 函数: addCosigner
  - 关键操作: require(!cosigner.active, "BCM: ALREADY_EXIST"), require(cosaddr != address(0), "BCM: ZERO_ADDRESS")
- **事件**: CosignerRemoved
  - 函数: removeCosigner
  - 关键操作: require(cosaddr != address(0), "BCM: ZERO_ADDRESS"), require(cosigner.active, "BCM: NOT_EXIST")
### det_chain: destination_chain
- **事件**: Exit1
  - 函数: exit
  - 关键操作: require(bytes32(logTopicRLPList[0].toUint()) == ENTER_EVENT_SIG, "BR: INVALID_EVT"), require(exitor == _msgSender(), "BR: NOT_ONWER"), require(amount != 0, "BR: ZERO_AMOUNT"), require(localChainId == _chainId, "BR: WRONG_TARGET_CHAIN"), require(extChainId != _chainId, "BR: WRONG_SOURCE_CHAIN"), require(!_commitments[commitment], "BR: COMMITMENT_KNOWN"), _commitments[commitment] = true
---
