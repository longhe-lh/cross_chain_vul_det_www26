# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TransitSwapped1
- **rel_chain**: callbytes
- **det_chain**: TransitSwapped1
### src_chain: Ethereum
- **事件**: TransitSwapped1
  - 函数: swap
  - 关键操作: require(desc.amount > 0, "TransitSwap: amount should be greater than 0");, require(desc.dstReceiver != address(0), "TransitSwap: receiver should be not address(0)");, require(desc.minReturnAmount > 0, "TransitSwap: minReturnAmount should be greater than 0");, (uint256 swapAmount, uint256 fee, uint256 beforeBalance) = _beforeSwap(preTradeModel, desc);, (bool success, bytes memory result) = _transit_swap.call{value:swapAmount}(abi.encodeWithSelector(0xccbe4007, callbytesDesc));, revert(RevertReasonParser.parse(result,"TransitSwap:"));, (uint256 returnAmount, uint256 postFee) = _afterSwap(preTradeModel, desc, beforeBalance);, if (postFee > fee) { fee = postFee; }
  - 函数: cross
  - 关键操作: require(callbytesDesc.calldatas.length > 0, "TransitSwap: data should be not zero");, require(desc.amount > 0, "TransitSwap: amount should be greater than 0");, require(desc.srcToken == callbytesDesc.srcToken, "TransitSwap: invalid callbytesDesc");, (uint256 swapAmount, uint256 fee, uint256 beforeBalance) = _beforeCross(desc);, (bool success, bytes memory result) = _transit_cross.call{value:swapAmount}(abi.encodeWithSelector(0xccbe4007, callbytesDesc));, revert(RevertReasonParser.parse(result,"TransitSwap:"));, require(IERC20(desc.srcToken).balanceOf(_transit_cross) >= beforeBalance, "TransitSwap: invalid cross");
### rel_chain: RelayChain
- **事件**: callbytes
  - 函数: callbytes
### det_chain: DestinationChain
- **事件**: TransitSwapped1
  - 函数: _emitTransit
  - 关键操作: emit TransitSwapped(desc.srcToken, desc.dstToken, desc.dstReceiver, msg.sender, preTradeModel, desc.amount, returnAmount, desc.minReturnAmount, fee, desc.toChainID, desc.channel, block.timestamp);
---
