import React from "react";
import { jsx as _jsx } from "react/jsx-runtime";
import { Dialog, DialogContent } from '../../ui/dialog';
export const ActionModal = ({ open, onClose, children }) => {
    return (_jsx(Dialog, { open: open, onOpenChange: onClose, children: _jsx(DialogContent, { children: children }) }));
};
