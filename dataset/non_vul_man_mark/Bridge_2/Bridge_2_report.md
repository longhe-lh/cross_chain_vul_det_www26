# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: Swap1
- **det_chain**: TokenMint1
### src_chain: source_chain
- **事件**: Swap1
  - 函数: swap
  - 关键操作: if (_tokenFrom == address(0x0) || _tokenTo == address(0x0)) revert ZeroAddress(), if (!chains[block.chainid].tokens[_tokenFrom]) revert IncorrectAction(_tokenFrom, false), if (!chains[_chainId].tokens[_tokenTo]) revert IncorrectAction(_tokenTo, false), _nonce++, ITokenForBridge(_tokenFrom).burn(msg.sender, _amount)
### rel_chain: relay_chain
- 无事件
### det_chain: destination_chain
- **事件**: TokenMint1
  - 函数: reedem
  - 关键操作: bytes32 signedHash = keccak256(abi.encodePacked(_tokenTo, _to, _amount, _nonce_)), bytes32 messageHash = signedHash.toEthSignedMessageHash(), address messageSender = messageHash.recover(_signature), if (messageSender != validator) revert IncorrectSignature(), ITokenForBridge(_tokenTo).mint(_to, _amount)
---
