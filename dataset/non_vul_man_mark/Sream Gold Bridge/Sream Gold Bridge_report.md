# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenMappedERC201, FxWithdrawERC202, FxDepositERC203
- **rel_chain**: NewFxMessage
- **det_chain**: TokenMapped1, FxWithdraw2, FxDeposit3
### src_chain: FxERC20RootTunnel
- **事件**: TokenMappedERC201
  - 函数: mapToken
  - 关键操作: require(rootToBridgeTokens[rootToken] == address(0x0), "FxERC20RootTunnel: ALREADY_MAPPED"), bytes memory message = abi.encode(MAP_TOKEN, abi.encode(rootToken, _bridgeToken)), _sendMessageToBridge(message), rootToBridgeTokens[rootToken] = _bridgeToken, emit TokenMappedERC20(rootToken, _bridgeToken)
- **事件**: FxWithdrawERC202
  - 函数: _processMessageFromBridge
  - 关键操作: (address rootToken, address bridgeToken, address to, uint256 amount) = abi.decode(data, (address, address, address, uint256)), require(rootToBridgeTokens[rootToken] == bridgeToken, "FxERC20RootTunnel: INVALID_MAPPING_ON_EXIT"), IERC20(rootToken).safeTransfer(to, amount), emit FxWithdrawERC20(rootToken, bridgeToken, to, amount)
- **事件**: FxDepositERC203
  - 函数: deposit
  - 关键操作: IERC20(rootToken).safeTransferFrom(msg.sender, address(this), amount), bytes memory message = abi.encode(DEPOSIT, abi.encode(rootToken, msg.sender, user, amount, data)), _sendMessageToBridge(message), emit FxDepositERC20(rootToken, msg.sender, user, amount)
### rel_chain: FxBridge
- **事件**: NewFxMessage
  - 函数: onStateReceive
  - 关键操作: require(msg.sender == address(0x0000000000000000000000000000000000001001), "Invalid sender", emit NewFxMessage(rootMessageSender, receiver, data), IFxMessageProcessor(receiver).processMessageFromRoot(stateId, rootMessageSender, data)
### det_chain: FxERC20BridgeTunnel
- **事件**: TokenMapped1
  - 函数: _processMessageFromRoot
  - 关键操作: (bytes32 syncType, bytes memory syncData) = abi.decode(data, (bytes32, bytes)), _mapToken(syncData)
- **事件**: FxWithdraw2
  - 函数: withdraw
  - 关键操作: _withdraw(bridgeToken, msg.sender, amount)
- **事件**: FxDeposit3
  - 函数: _syncDeposit
  - 关键操作: address bridgeToken = rootToBridgeToken[rootToken], require(bridgeToken != address(0), "Bridge Token cannot be zero address"), IFxERC20 bridgeTokenContract = IFxERC20(bridgeToken), bridgeTokenContract.mint(to, amount)
---
