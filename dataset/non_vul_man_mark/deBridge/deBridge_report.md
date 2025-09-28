# 跨链桥合约分析报告
## 跨链桥: DeBridgeGate
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: send1, claim1
- **rel_chain**: submit1
- **det_chain**: claim1
### src_chain: source_chain
- **事件**: send1
  - 函数: send
  - 关键操作: _send(_permit, _tokenAddress, _amount, _chainIdTo, _useAssetFee)
- **事件**: claim1
  - 函数: claim
  - 关键操作: _checkConfirmations(submissionId, _debridgeId, _amount, _signatures);, if (isSubmissionUsed[submissionId]) revert SubmissionUsed();, isSubmissionUsed[submissionId] = true;
### rel_chain: relay_chain
- **事件**: submit1
  - 函数: submit
  - 关键操作: if (getOracleInfo[oracle].isValid) { ... }, emit Confirmed(_submissionId, oracle);, if (confirmations >= needConfirmations && currentRequiredOraclesCount >= requiredOraclesCount) { ... }
### det_chain: destination_chain
- **事件**: claim1
  - 函数: claim
  - 关键操作: _claim(_debridgeId, _receiver, _amount, _chainIdFrom, _autoParams);
---
