# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: TokenLocked1, TokenLocked2, TokenLocked3, TokenLocked4
- **rel_chain**: CallResult, CallerUnMatched
- **det_chain**: TokenUnlocked1, TokenUnlocked2, TokenUnlocked3, TokenUnlocked4
### src_chain: Ethereum
- **事件**: TokenLocked1
  - 函数: lockAndRemoteIssuing
  - 关键操作: require(IERC20(token).transferFrom(msg.sender, address(this), amount), "Backing:transfer tokens failed"), IWToken(wToken).deposit{value: amount}(), IERC20(token).mint(recipient, amount)
- **事件**: TokenLocked2
  - 函数: lockAndRemoteIssuing
  - 关键操作: require(IERC20(token).transferFrom(msg.sender, address(this), amount), "Backing:transfer tokens failed"), IERC20(token).mint(recipient, amount)
- **事件**: TokenLocked3
  - 函数: lockAndRemoteIssuing
  - 关键操作: IERC1155(token).safeBatchTransferFrom(msg.sender, address(this), ids, amounts, ""), IErc1155MappingToken(mappingToken).mintBatch(recipient, ids, amounts)
- **事件**: TokenLocked4
  - 函数: lockAndRemoteIssuing
  - 关键操作: IERC721(token).transferFrom(msg.sender, address(this), ids[idx]), IErc721MappingToken(mappingToken).mint(recipient, tokenId)
### rel_chain: RelayChain
- **事件**: CallResult
  - 函数: execute
  - 关键操作: require(gateway.validateContractCall(_commandId, _sourceChain, _sourceAddress, keccak256(_payload)), "invalid contract call"), require(_sourceAddress.toAddress() == trustedRemotes[_sourceChain], "invalid remote messager")
- **事件**: CallerUnMatched
  - 函数: receiveMessage
  - 关键操作: require(srcChainId == remoteMessager.msglineRemoteChainId, "invalid remote chainid"), require(remoteMessager.messager == _xmsgSender(), "invalid remote messager")
### det_chain: Polygon
- **事件**: TokenUnlocked1
  - 函数: recvMessage
  - 关键操作: require(inboundLane == msg.sender && remoteEndpoint == sourceAccount, "cross_chain_filter"), require(hasRole(CALLEE_ROLE, receiver), "receiver is not callee"), (bool result,) = receiver.call{value: 0}(payload)
- **事件**: TokenUnlocked2
  - 函数: recvMessage
  - 关键操作: require(inboundLane == msg.sender && remoteEndpoint == sourceAccount, "cross_chain_filter"), require(hasRole(CALLEE_ROLE, receiver), "receiver is not callee"), (bool result,) = receiver.call(message)
- **事件**: TokenUnlocked3
  - 函数: recvMessage
  - 关键操作: require(inboundLane == msg.sender && remoteEndpoint == sourceAccount, "cross_chain_filter"), require(hasRole(CALLEE_ROLE, receiver), "receiver is not callee"), (bool result,) = receiver.call(message)
- **事件**: TokenUnlocked4
  - 函数: recvMessage
  - 关键操作: require(inboundLane == msg.sender && remoteEndpoint == sourceAccount, "cross_chain_filter"), require(hasRole(CALLEE_ROLE, receiver), "receiver is not callee"), (bool result,) = receiver.call(message)
---
