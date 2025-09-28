# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: LiFiTransferStarted1
- **det_chain**: LiFiTransferCompleted1
### src_chain: source_chain
- **事件**: LiFiTransferStarted1
  - 函数: startBridgeTokensViaAmarok
  - 关键操作: LibAsset.depositAsset(_bridgeData.sendingAssetId, _bridgeData.minAmount), _startBridge(_bridgeData, _amarokData)
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: LiFiTransferCompleted1
  - 函数: execute
---
