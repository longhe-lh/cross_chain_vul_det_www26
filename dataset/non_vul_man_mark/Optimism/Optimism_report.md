# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: ETHBridgeInitiated1, ERC20BridgeInitiated2
- **rel_chain**: relayMessage
- **det_chain**: ETHBridgeFinalized1, ERC20BridgeFinalized2
### src_chain: L1
- **事件**: ETHBridgeInitiated1
  - 函数: _initiateBridgeETH
  - 关键操作: require(msg.value == _amount, "StandardBridge: bridging ETH must include sufficient ETH value"), deposits[_l1Token][_l2Token] = deposits[_l1Token][_l2Token] + _amount;
- **事件**: ERC20BridgeInitiated2
  - 函数: _initiateBridgeERC20
  - 关键操作: IERC20(_l1Token).safeTransferFrom(_from, address(this), _amount);, deposits[_l1Token][_l2Token] = deposits[_l1Token][_l2Token] + _amount;
### rel_chain: RelayChain
- **事件**: relayMessage
  - 函数: relayMessage
  - 关键操作: getCrossDomainMessenger().sendMessage(...), require(success, "StandardBridge: ETH transfer failed")
### det_chain: L2
- **事件**: ETHBridgeFinalized1
  - 函数: finalizeBridgeETH
  - 关键操作: SafeCall.call(_to, gasleft(), _amount, hex"")
- **事件**: ERC20BridgeFinalized2
  - 函数: finalizeBridgeERC20
  - 关键操作: OptimismMintableERC20(_localToken).mint(_to, _amount);, IERC20(_localToken).safeTransfer(_to, _amount);
---
