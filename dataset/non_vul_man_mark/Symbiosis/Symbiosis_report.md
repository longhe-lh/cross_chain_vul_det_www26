# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: SynthesizeRequest1, RevertBurnRequest2
- **rel_chain**: transmitRequestV2, receiveRequestV2
- **det_chain**: MintSyntheticToken1, revertBurn2
### src_chain: Portal
- **事件**: SynthesizeRequest1
  - 函数: synthesize
  - 关键操作: require(tokenWhitelist[_token], "Symb: unauthorized token"), require(_amount >= tokenThreshold[_token], "Symb: amount under threshold"), TransferHelper.safeTransferFrom(_token, _msgSender(), address(this), _amount), sendSynthesizeRequest
- **事件**: RevertBurnRequest2
  - 函数: revertBurnRequest
  - 关键操作: require(unsynthesizeStates[externalID] != UnsynthesizeState.Unsynthesized, "Symb: Real tokens already transfered"), unsynthesizeStates[externalID] = UnsynthesizeState.RevertRequest, IBridge(bridge).transmitRequestV2(out, _receiveSide, _oppositeBridge, _chainId)
### rel_chain: IBridge
- **事件**: transmitRequestV2
  - 函数: transmitRequestV2
- **事件**: receiveRequestV2
  - 函数: receiveRequestV2
### det_chain: Synthesis
- **事件**: MintSyntheticToken1
  - 函数: mintSyntheticToken
  - 关键操作: _transfer, emit Transfer
- **事件**: revertBurn2
  - 函数: revertBurn
  - 关键操作: require(txState.state == RequestState.Sent, "Symb: state not open or tx does not exist"), txState.state = RequestState.Reverted, TransferHelper.safeTransfer(txState.rtoken, txState.recipient, txState.amount - _stableBridgingFee)
---
