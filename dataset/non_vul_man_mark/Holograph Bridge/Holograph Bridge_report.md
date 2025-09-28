# 跨链桥合约分析报告
## 跨链桥: HolographBridge
**跨链类型**: heterogeneous
### 角色分析
- **src_chain**: bridgeIn1, bridgeOut2
- **rel_chain**: lzReceive
- **det_chain**: bridgeIn1, bridgeOut2
### src_chain: source chain
- **事件**: bridgeIn1
  - 函数: bridgeIn
  - 关键操作: require(!_exists(tokenId), 'ERC721: token already exists');, delete _burnedTokens[tokenId];, _mint(to, tokenId);, if (_isEventRegistered(HolographERC721Event.bridgeIn)) { require(_sourceCall(abi.encodeWithSelector(HolographedERC721.bridgeIn.selector, fromChain, from, to, tokenId, data)), 'HOLOGRAPH: bridge in failed'; }
- **事件**: bridgeOut2
  - 函数: bridgeOut
  - 关键操作: require(to != address(0), 'ERC721: zero address');, require(_isApproved(sender, tokenId), 'ERC721: sender not approved');, require(from == _tokenOwner[tokenId], 'ERC721: from is not owner');, if (_isEventRegistered(HolographERC721Event.bridgeOut)) {, bytes memory sourcePayload = abi.encodeWithSelector(HolographedERC721.bridgeOut.selector, toChain, from, to, tokenId);, assembly { mstore(add(sourcePayload, add(mload(sourcePayload), 0x20)), caller()) }, let result := call(gas(), sload(_sourceContractSlot), callvalue(), add(sourcePayload, 0x20), add(mload(sourcePayload), 0x20), 0, 0), returndatacopy(data, 0x20, sub(returndatasize(), 0x20)), switch result case 0 { revert(0, returndatasize()) }
### rel_chain: relay chain
- **事件**: lzReceive
  - 函数: lzReceive
  - 关键操作: require(eq(sload(_lZEndpointSlot), caller()), 'HOLOGRAPH: LZ only endpoint');, calldatacopy(add(ptr, 0x0c), _srcAddress.offset, _srcAddress.length), switch eq(mload(ptr), address()) case 0 { revert('HOLOGRAPH: unauthorized sender'); }, assembly { let result := call(gas(), sload(_sourceContractSlot), callvalue(), 0, add(calldatasize(), 0x20), 0, 0) }, switch result case 0 { revert(0, returndatasize()) } default { return(0, returndatasize()) }
### det_chain: destination chain
- **事件**: bridgeIn1
  - 函数: bridgeIn
  - 关键操作: require(!_exists(tokenId), 'ERC721: token already exists');, delete _burnedTokens[tokenId];, _mint(to, tokenId);, if (_isEventRegistered(HolographERC721Event.bridgeIn)) { require(_sourceCall(abi.encodeWithSelector(HolographedERC721.bridgeIn.selector, fromChain, from, to, tokenId, data)), 'HOLOGRAPH: bridge in failed'; }
- **事件**: bridgeOut2
  - 函数: bridgeOut
  - 关键操作: require(to != address(0), 'ERC721: zero address');, require(_isApproved(sender, tokenId), 'ERC721: sender not approved');, require(from == _tokenOwner[tokenId], 'ERC721: from is not owner');, if (_isEventRegistered(HolographERC721Event.bridgeOut)) {, bytes memory sourcePayload = abi.encodeWithSelector(HolographedERC721.bridgeOut.selector, toChain, from, to, tokenId);, assembly { mstore(add(sourcePayload, add(mload(sourcePayload), 0x20)), caller()) }, let result := call(gas(), sload(_sourceContractSlot), callvalue(), add(sourcePayload, 0x20), add(mload(sourcePayload), 0x20), 0, 0), returndatacopy(data, 0x20, sub(returndatasize(), 0x20)), switch result case 0 { revert(0, returndatasize()) }
---
