# 跨链桥合约分析报告
## 跨链桥: bridge_name
**跨链类型**: homogeneous
### 角色分析
- **src_chain**: TokenTransferFungible1, TokenTransferNonFungible2, TokenTransferMixedFungible3
- **rel_chain**: MessageSent, BroadcastSent, MessageReceived
- **det_chain**: TokenClaimedFungible1, TokenClaimedNonFungible2, TokenClaimedMixedFungible3
### src_chain: SourceChain
- **事件**: TokenTransferFungible1
  - 函数: transferFungible
  - 关键操作: IERC20Upgradeable(token).transferFrom(_msgSender(), address(this), amount)
- **事件**: TokenTransferNonFungible2
  - 函数: transferNonFungible
  - 关键操作: IERC721Upgradeable(_token).transferFrom(_msgSender(), address(this), _tokenId)
- **事件**: TokenTransferMixedFungible3
  - 函数: transferMixedFungible
  - 关键操作: IERC1155Upgradeable(_token).safeTransferFrom(_msgSender(), address(this), _tokenId, _amount, "")
### rel_chain: RelayChain
- **事件**: MessageSent
  - 函数: sendMessage
  - 关键操作: _sendMessage(_messageId, _destination, _recipient, _receipt, _message)
- **事件**: BroadcastSent
  - 函数: sendBroadcast
  - 关键操作: _sendBroadcast(_messageId, _receipt, _message)
- **事件**: MessageReceived
  - 函数: relayMessage
  - 关键操作: block.number <= maxBlock, hash.recover(signature) == feeVerifier
### det_chain: DestinationChain
- **事件**: TokenClaimedFungible1
  - 函数: bridgeClaimFungible
  - 关键操作: IERC20Upgradeable(_token).transfer(_to, _amount)
- **事件**: TokenClaimedNonFungible2
  - 函数: bridgeClaimNonFungible
  - 关键操作: IERC721Bridgable(_token).bridgeMint(_to, _tokenId), IERC721Bridgable(_token).transferFrom(address(this), _to, _tokenId)
- **事件**: TokenClaimedMixedFungible3
  - 函数: bridgeClaimMixedFungible
  - 关键操作: IERC1155Bridgable(token).safeTransferFrom(address(this), to, tokenId, balanceToTransfer, ""), IERC1155Bridgable(token).bridgeMint(to, tokenId, balanceToMint)
---
