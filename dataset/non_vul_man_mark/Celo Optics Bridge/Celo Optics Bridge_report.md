# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: Send1
- **rel_chain**: Dispatch, Update, DoubleUpdate, ImproperUpdate
- **det_chain**: Process1
### src_chain: source_chain
- **事件**: Send1
  - 函数: send
  - 关键操作: require(_amount > 0, "!amnt"), require(_recipient != bytes32(0), "!recip"), IERC20 _bridgeToken = IERC20(_token), if (_isLocalOrigin(_bridgeToken)), _bridgeToken.safeTransferFrom(msg.sender, address(this), _amount), _downcast(_bridgeToken).burn(msg.sender, _amount), Home(xAppConnectionManager.home()).dispatch(_destination, _remote, BridgeMessage.formatMessage(_formatTokenId(_token), _action))
### rel_chain: relay_chain
- **事件**: Dispatch
  - 函数: dispatch
  - 关键操作: require(_messageBody.length <= MAX_MESSAGE_BODY_BYTES, "msg too long"), uint32 _nonce = nonces[_destinationDomain], nonces[_destinationDomain] = _nonce + 1, bytes memory _message = Message.formatMessage(localDomain, bytes32(uint256(uint160(msg.sender))), _nonce, _destinationDomain, _recipientAddress, _messageBody), bytes32 _messageHash = keccak256(_message), tree.insert(_messageHash), queue.enqueue(root())
- **事件**: Update
  - 函数: update
  - 关键操作: require(_isUpdaterSignature(_oldRoot, _newRoot, _signature), "!updater sig"), require(_oldRoot == committedRoot, "not a current update")
- **事件**: DoubleUpdate
  - 函数: doubleUpdate
  - 关键操作: require(state != States.Failed, "failed state")
- **事件**: ImproperUpdate
  - 函数: improperUpdate
  - 关键操作: require(_isUpdaterSignature(_oldRoot, _newRoot, _signature), "!updater sig"), require(_oldRoot == committedRoot, "not a current update")
### det_chain: destination_chain
- **事件**: Process1
  - 函数: proveAndProcess
  - 关键操作: require(prove(keccak256(_message), _proof, _index), "!prove")
---
