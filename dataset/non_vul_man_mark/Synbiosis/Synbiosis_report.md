# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SynthesizeRequest1, BurnRequest2
- **rel_chain**: transmitRequestV2
- **det_chain**: MintSyntheticToken1, Unsynthesize2
### src_chain: PortalChain
- **事件**: SynthesizeRequest1
  - 函数: synthesize
  - 关键操作: require(tokenWhitelist[_token], "Symb: unauthorized token"), require(_amount >= tokenThreshold[_token], "Symb: amount under threshold"), TransferHelper.safeTransferFrom(_token, _msgSender(), address(this), _amount)
- **事件**: BurnRequest2
  - 函数: burnSyntheticToken
  - 关键操作: require(_amount >= tokenThreshold[_stoken], "Symb: amount under threshold"), ISyntFabric(fabric).unsynthesize(_msgSender(), _amount, _stoken)
### rel_chain: RelayChain
- **事件**: transmitRequestV2
  - 函数: transmitRequestV2
  - 关键操作: emit OracleRequest(address(this), _callData, _receiveSide, _oppositeBridge, _chainId)
### det_chain: SynthesisChain
- **事件**: MintSyntheticToken1
  - 函数: mintSyntheticToken
  - 关键操作: require(syntReprAddr != address(0), "Symb: There is no synt representation for this token"), ISyntFabric(fabric).synthesize(_to, _amount - _stableBridgingFee, syntReprAddr), ISyntFabric(fabric).synthesize(bridge, _stableBridgingFee, syntReprAddr)
- **事件**: Unsynthesize2
  - 函数: unsynthesize
  - 关键操作: balanceOf[_token] = balanceOf[_token] - _amount, TransferHelper.safeTransfer(_token, _to, _amount - _stableBridgingFee), TransferHelper.safeTransfer(_token, bridge, _stableBridgingFee)
---
