# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: transferTokens1, wrapAndTransferETH2, attestToken3
- **rel_chain**: parseAndVerifyVM, verifyVM
- **det_chain**: completeTransfer1, completeTransferAndUnwrapETH2, updateWrapped3
### src_chain: source_chain
- **事件**: transferTokens1
  - 函数: transferTokens
  - 关键操作: require(msg.value == wormhole().messageFee(), "invalid fee"), require(wormholeFee < msg.value, "value is smaller than wormhole fee"), require(arbiterFee <= amount, "fee is bigger than amount minus wormhole fee")
- **事件**: wrapAndTransferETH2
  - 函数: wrapAndTransferETH
  - 关键操作: require(wormholeFee < msg.value, "value is smaller than wormhole fee"), require(arbiterFee <= amount, "fee is bigger than amount minus wormhole fee")
- **事件**: attestToken3
  - 函数: attestToken
### rel_chain: relay_chain
- **事件**: parseAndVerifyVM
  - 函数: parseAndVerifyVM
  - 关键操作: require(valid, reason)
### det_chain: destination_chain
- **事件**: completeTransfer1
  - 函数: completeTransfer
- **事件**: completeTransferAndUnwrapETH2
  - 函数: completeTransferAndUnwrapETH
- **事件**: updateWrapped3
  - 函数: updateWrapped
  - 关键操作: require(valid, reason), require(verifyBridgeVM(vm), "invalid emitter")
---
